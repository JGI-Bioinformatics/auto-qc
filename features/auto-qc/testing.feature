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
           value: <var>
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 0.1.0
     thresholds:
     - node:
         id: test_1
         analysis: object_1
         operator: <operator>
         args: ['metric_1/value', <threshold>]
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
      | var | operator     | threshold | result |
      | 1   | greater_than | 0         | FAIL   |
      | 1   | greater_than | 2         | PASS   |
      | 1   | less_than    | 2         | FAIL   |
      | 1   | less_than    | 0         | PASS   |

  Scenario Outline: Testing multiple thresholds
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: <var_1>
     - analysis: object_2
       outputs:
         metric_2:
           value: <var_2>
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 0.1.0
     thresholds:
     - node:
         id: test_1
         analysis: object_1
         operator: greater_than
         args: ['metric_1/value', <threshold_1>]
     - node:
         id: test_2
         analysis: object_2
         operator: greater_than
         args: ['metric_2/value', <threshold_2>]
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

  Examples: Multiple thresholds
      | var_1 | var_2 | threshold_1 | threshold_2 | result |
      | 1     | 1     | 2           | 2           | PASS   |
      | 3     | 1     | 2           | 2           | FAIL   |
      | 3     | 3     | 2           | 2           | FAIL   |

  Scenario: Generating yaml description of threshold tests
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: 1
     - analysis: object_2
       outputs:
         metric_2:
           value: 2
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 0.1.0
     thresholds:
     - node:
         id: test_1
         analysis: object_1
         operator: greater_than
         args: ['metric_1/value', 1]
     - node:
         id: test_2
         analysis: object_2
         operator: greater_than
         args: ['metric_2/value', 0]
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --yaml-output    |               |
   Then the standard error should be empty
    And the standard out should equal:
      """
      fail: true
      metadata:
        version:
          auto-qc: 0.1.0
      thresholds:
      - node:
          analysis: object_1
          args:
          - metric_1/value
          - 1
          fail: false
          id: test_1
          operator: greater_than
      - node:
          analysis: object_2
          args:
          - metric_2/value
          - 0
          fail: true
          id: test_2
          operator: greater_than


      """
     And the exit code should be 0
