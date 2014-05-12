Feature: Using the auto-qc tool
  In order to determine whether a sample passes QC
  The auto-qc tool can be used to
  Test quality thresholds

  Scenario: The given analysis file does not exist
   Given I create the file "thresholds.yml"
    When I run the command "auto-qc" with the arguments:
       | key              | value          |
       | --analysis_file  | none           |
       | --threshold_file | thresholds.yml |
   Then the standard error should contain:
      """
      File not found: 'none'.

      """
     And the exit code should be 1

  Scenario: The given thresholds file does not exist
   Given I create the file "analysis.yml"
    When I run the command "auto-qc" with the arguments:
       | key              | value          |
       | --analysis_file  | analysis.yml   |
       | --threshold_file | none           |
   Then the standard error should contain:
      """
      File not found: 'none'.

      """
     And the exit code should be 1

  Scenario: Testing a single passing threshold
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: 1
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 0.0.0
     thresholds:
     - node:
         analysis: object_1
         operator: greater_than
         args: ['metric_1/value', 1]
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
   Then the standard error should be empty
    And the standard out should contain:
      """
      PASS

      """
     And the exit code should be 0
