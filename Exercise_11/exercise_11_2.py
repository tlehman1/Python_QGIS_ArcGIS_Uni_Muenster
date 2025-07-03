class ToolValidator:
  # Class to add custom behavior and properties to the tool and tool parameters.

    def __init__(self):
        # Set self.params for use in other validation methods.
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        # Customize parameter properties. This method gets called when the
        # tool is opened.
        return

    def updateParameters(self):
        # if feature class is set,provide Values for Parameter 1: name_field       
        if self.params[1].altered:
            # Use the Describe Function to get Details (field names) for Input FC
            fields = arcpy.Describe(self.params[1]).fields
            field_names = [x.name for x in fields]
            # set the field names as filter for parameter [1]
            self.params[2].filter.list = field_names

        # if name field is selected provide values (all unique field values) for parameter 2: name_value
        if self.params[2].altered and self.params[1].altered:
            # get a table of the unique values for the name field
            arcpy.analysis.Frequency(in_table=self.params[1].value,out_table='in_memory\\freq_table',frequency_fields=self.params[2].value)
            name_values = [row[0] for row in arcpy.da.SearchCursor(in_table='in_memory\\freq_table', field_names=[self.params[2].value])]
            #delete the table in memory
            arcpy.Delete_management('in_memory\\freq_table')
            #set the parameter filter list
            self.params[3].filter.list = name_values
        
        return

    def updateMessages(self):
        # Modify the messages created by internal validation for each tool
        # parameter. This method is called after internal validation.
        return

    # def isLicensed(self):
    #     # Set whether the tool is licensed to execute.
    #     return True

    # def postExecute(self):
    #     # This method takes place after outputs are processed and
    #     # added to the display.
    #     return
