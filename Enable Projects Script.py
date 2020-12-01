# Databricks notebook source
# MAGIC %md
# MAGIC ### Enabling Projects
# MAGIC Please run the first cell to initialize widgets. Enter the respective fields in the widget inputs and run this notebook.
# MAGIC 
# MAGIC - `Admin Token`: token created by workspace admin in User Settings > Access Tokens
# MAGIC - `Databricks Instance`: workspace URL of Databricks deployment (https://docs.databricks.com/workspace/workspace-details.html#workspace-url)
# MAGIC - `Enable Projects`: `true` to enable, `false` to disable

# COMMAND ----------

# Initialize input widgets
dbutils.widgets.removeAll()
dbutils.widgets.text("admin-token", "", "Admin Token")
dbutils.widgets.text("databricks-instance", "", "Databricks Instance")
dbutils.widgets.text("enable-projects", "true", "Enable Projects")

# COMMAND ----------

# Feel free to directly set the environment variables here, instead of setting them through widgets
import os
os.environ["ADMIN_TOKEN"] = dbutils.widgets.get("admin-token")
os.environ["DATABRICKS_INSTANCE"] = dbutils.widgets.get("databricks-instance")
os.environ["ENABLE_PROJECTS"] = dbutils.widgets.get("enable-projects")

# COMMAND ----------

# MAGIC %md
# MAGIC Optional check that environment variables are set correctly

# COMMAND ----------

# MAGIC %sh
# MAGIC echo $ADMIN_TOKEN
# MAGIC echo $DATABRICKS_INSTANCE
# MAGIC echo $ENABLE_PROJECTS

# COMMAND ----------

# MAGIC %md
# MAGIC #### Check that there is no folder named "Projects" in the root directory
# MAGIC You should get a `RESOURCE_DOES_NOT_EXIST` response here. If you don't, rename or delete the "Projects" folder in the root directory and migrate the jobs.

# COMMAND ----------

# MAGIC %sh
# MAGIC curl -X GET -H 'Authorization: Bearer '$ADMIN_TOKEN'' https://$DATABRICKS_INSTANCE/api/2.0/workspace/get-status -d '{ "path": "/Projects" }'

# COMMAND ----------

# MAGIC %md
# MAGIC #### Enable Projects!
# MAGIC This flips the feature flag. Projects will be enabled on webapp restart for ST, tenant unload for MT.

# COMMAND ----------

# MAGIC %sh
# MAGIC curl -X PATCH -H 'Authorization: Bearer '$ADMIN_TOKEN'' https://$DATABRICKS_INSTANCE/api/2.0/workspace-conf -d '{ "enableProjectTypeInWorkspace": "'$ENABLE_PROJECTS'" }'

# COMMAND ----------

# MAGIC %md
# MAGIC #### Check that flag has been set
# MAGIC If command returns with `{"enableProjectTypeInWorkspace":"true"}`, you should be all set.

# COMMAND ----------

# MAGIC %sh
# MAGIC curl -X GET -H 'Authorization: Bearer '$ADMIN_TOKEN'' https://$DATABRICKS_INSTANCE/api/2.0/workspace-conf?keys=enableProjectTypeInWorkspace