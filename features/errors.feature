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

  Scenario Outline: Unknown node type
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
         auto-qc: 0.3.0
     thresholds:
     -
       - node: <operator>
         value: greater_than
       - node: <variable>
         value: 'object_1/metric_1/value'
       - node: <literal>
         value: 1
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
   Then the standard error should contain:
      """
      Unknown node type: "<error>"

      """
    And the exit code should be 1
    And the standard out should be empty

  Examples: Operators
      | operator | variable     | literal | error   |
      | operator | variable     | unknown | unknown |
      | operator | unknown      | literal | unknown |
      | unknown  | variable     | literal | unknown |
