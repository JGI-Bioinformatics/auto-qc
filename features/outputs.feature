Feature: Printing different output formats
  In order to visualise the QC results
  The auto-qc tool can generate different output formats

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
         auto-qc: 0.2.1
     thresholds:
     - node:
         id: test_1
         analysis: object_1
         operator: greater_than
         threshold: 1
         metric: 'metric_1/value'
     - node:
         id: test_2
         analysis: object_2
         operator: greater_than
         threshold: 1
         metric: 'metric_2/value'
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --yaml-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      fail: true
      metadata:
        version:
          auto-qc: 0.2.1
      thresholds:
      - node:
          analysis: object_1
          fail: false
          id: test_1
          metric: metric_1/value
          metric_value: 1
          operator: greater_than
          threshold: 1
      - node:
          analysis: object_2
          fail: true
          id: test_2
          metric: metric_2/value
          metric_value: 2
          operator: greater_than
          threshold: 1

      """

  Scenario: Generating a text description of the threshold tests
   Given I create the file "analysis.yml" with the contents:
     """
     - analysis: object_1
       outputs:
         metric_1:
           value: 1
     - analysis: object_2
       outputs:
         metric_2:
           value: 2000000
     - analysis: object_3
       outputs:
         metric_3:
           value: 1
     """
     And I create the file "threshold.yml" with the contents:
     """
     metadata:
       version:
         auto-qc: 0.2.1
     thresholds:
     - node:
         id: test_1
         analysis: object_1
         operator: greater_than
         threshold: 1
         metric: 'metric_1/value'
     - node:
         id: longer_test_name
         analysis: object_2
         operator: greater_than
         threshold: 1
         metric: 'metric_2/value'
     - node:
         id: test_3
         analysis: object_3
         operator: greater_than
         threshold: 1.5
         metric: 'metric_3/value'
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
       | --text-output    |               |
   Then the standard error should be empty
    And the exit code should be 0
    And the standard out should equal:
      """
      Status: FAIL

                          Failure At      Actual

      test_1:                    > 1           1
      longer_test_name:          > 1   2,000,000   FAIL
      test_3:                  > 1.5           1

      Auto QC Version: 0.2.1

      """
