Feature: Using the auto-qc tool
  In order to determine whether a sample passes QC
  The auto-qc tool can be used to
  Test quality thresholds

  Scenario Outline: Threshold operators
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: <variable>
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 0.3.0
     thresholds:
     -
       - <operator>
       - :object_1/metric_1/value
       - <literal>
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should contain:
      """
      <result>

      """

  Examples: Operators
      | variable | operator     | literal | result |
      | 1        | greater_than | 0       | FAIL   |
      | 1        | greater_than | 2       | PASS   |
      | 1        | less_than    | 2       | FAIL   |
      | 1        | less_than    | 0       | PASS   |
