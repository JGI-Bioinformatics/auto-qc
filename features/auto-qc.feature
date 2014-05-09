Feature: Using the auto-qc tool
  In order to determine whether a sample passes QC
  The auto-qc tool can be used to
  Test quality thresholds

  Scenario: The given analysis file does not exist
    When I run the command "auto-qc" with the arguments:
       | key             | value      |
       | --analysis_file | none       |
   Then the standard error should contain:
      """
      File not found: 'none'.

      """
     And the exit code should be 1
