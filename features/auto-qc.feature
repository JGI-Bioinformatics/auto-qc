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

  @wip
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

  Scenario: Testing a multiple passing thresholds
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
         auto-qc: 0.0.0
     thresholds:
     - node:
         analysis: object_1
         operator: greater_than
         args: ['metric_1/value', 1]
     - node:
         analysis: object_2
         operator: greater_than
         args: ['metric_2/value', 5]
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

  Scenario: Testing a single failing threshold
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
         args: ['metric_1/value', 0]
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
   Then the standard error should be empty
    And the standard out should contain:
      """
      FAIL

      """
     And the exit code should be 0

  Scenario: Testing multiple failing thresholds
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
         auto-qc: 0.0.0
     thresholds:
     - node:
         analysis: object_1
         operator: greater_than
         args: ['metric_1/value', 0]
     - node:
         analysis: object_2
         operator: greater_than
         args: ['metric_2/value', 0]
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
   Then the standard error should be empty
    And the standard out should contain:
      """
      FAIL

      """
     And the exit code should be 0

  Scenario: Testing some failing thresholds
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
         auto-qc: 0.0.0
     thresholds:
     - node:
         analysis: object_1
         operator: greater_than
         args: ['metric_1/value', 1]
     - node:
         analysis: object_2
         operator: greater_than
         args: ['metric_2/value', 0]
     """
    When I run the command "auto-qc" with the arguments:
       | key              | value         |
       | --analysis_file  | analysis.yml  |
       | --threshold_file | threshold.yml |
   Then the standard error should be empty
    And the standard out should contain:
      """
      FAIL

      """
     And the exit code should be 0

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
         auto-qc: 0.0.0
     thresholds:
     - node:
         analysis: object_1
         operator: greater_than
         args: ['metric_1/value', 1]
     - node:
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
    And the standard out should contain:
      """
      metadata:
        version:
          auto-qc: 0.0.0
      pass: false
      thresholds:
       - node:
           analysis: object_1
           args: ['metric_1/value', 1]
           pass: true
           operator: greater_than
       - node:
           analysis: object_2
           args: ['metric_2/value', 0]
           pass: false
           operator: greater_than

      """
     And the exit code should be 0
