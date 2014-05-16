Feature: Error messages for incorrect use of auto-qc
  In order to correctly use the auto-qc tool
  The auto-qc provides useful errors
  So that the user use the modify their usage

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

  @wip
  Scenario: The given value does not exist
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
         auto-qc: 0.1.0
     thresholds:
     - node:
         id: test_threshold
         analysis: object_1
         operator: greater_than
         args: ['metric_1/non_path', 1]
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
   Then the standard out should be empty
    And the standard error should equal:
      """
      No matching path 'metric_1/non_path' found for node 'test_threshold.'

      """
    And the exit code should be 1

  Scenario: The given analysis does not exist
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
         auto-qc: 0.1.0
     thresholds:
     - node:
         id: test_threshold
         analysis: non_object
         operator: greater_than
         args: ['metric_1/value', 1]
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
   Then the standard out should be empty
    And the standard error should equal:
      """
      No matching analysis 'non_object' found for node 'test_threshold.'

      """
    And the exit code should be 1
