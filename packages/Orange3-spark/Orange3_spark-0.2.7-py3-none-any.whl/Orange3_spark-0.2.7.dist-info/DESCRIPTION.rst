Madrid, Spain.
Author: Jose Antonio Martin H. <xjamartinh@gmail.com>

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description: Orange3-Spark
        =============
        
        A set of widgets for Orange data mining suite to work with Apache Spark ML API.
        
        
        Requirements
        ------------
        
         - Python >= 3.4
         - Pandas
         - Orange 3
        
        Please follow the instruction to install Orange 3 first.
        
        The main Orange project is hosted at: https://github.com/biolab/orange3
        Download from: http://orange.biolab.si
        
        
        Features
        --------
        
          * A Spark Context.
          * A Hive Table.
          * A Dataframe from an SQL Query.
          * A Dataset Builder, basically a call to VectorAssembler, this is usefull before sending data to Estimators.
          * Transformers from the feature module.
          * Estimators from classification module.
          * Estimators from regression module.
          * Estimators from clustering module.
          * Evaluation from evaluator module.
          * A PySpark script executor + PySpark console.
          * DataFrame transformes for Pandas and Orangle Tables
        
        ... more coming soon!
        
        
        Installing
        ----------
        
        First, you need to have Apache Spark installed. Follow the instructions here:
        http://spark.apache.org/docs/latest/
        
        Then you can do:
        
            pip install Orange3-spark
        
        or install the add-on from the Orange's Options | Add-ons menu. Note, if
        installing from Add-ons menu, the installation may fail if not all requirements
        are satisfiable.
        
        If you require ODBC connectivity, you need to install `pyodbc`
        (which requires `sql.h` available if built with `pip` â€“
        that's `unixodbc-dev` package on Linux).
        
        If install is ok, you should see a new section in Orange containing a series of widgets from Spark ML API.
        
Keywords: orange3 add-ons,Spark,Spark ML,Machine Learning
Platform: UNKNOWN
