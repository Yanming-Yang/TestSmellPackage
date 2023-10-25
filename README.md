## 1 Test Smell

- **Empirical_SO_post_data.xlsx** contains all relevant posts we collect from Stack Overflow and data extracted from these posts.
- **TestSmellDetector** includes the source code of our detector.
- **project_list.txt** shows all projects which we use to evaluate the prevalence of our detector.

## 2 TestSmellDetector

### 2.1 Running Environment
Our detector is written in Python3.9 and transforms source code into AST by using *javalang* package **[GitHub:Javalang](https://github.com/c2nes/javalang)**.

### 2.2 How to use the detector
Our detector is easy to use.
You can run the source file *''main_detector.py''** with two parameters *''-project''* and *''-test_smell_types''*.

The first parameter is the path of the project you want to detect and it only allows one project (i.e., one value) at every turn.

The second parameter is the types of test smells you want to detect from your project.
This parameter supports multiple values and the value range is from 1 to 7.

Where ''1'' denotes detecting **PMT** test smells;

      ''2'' denotes detecting **NDT** test smells;

      ''3'' denotes detecting **PTO** test smells (e.g., bad test code organization (BTCO));

      ''4'' denotes detecting **POW** test smells;

      ''5'' denotes detecting **AL** test smells;

      ''6'' denotes detecting **RT** test smell;

      ''7'' denotes detecting another type of **PTO** test smells (i.e., test code in production code(TCPC));

Thus, you can input ***''main_detector.py -project fastjson -test_smell_types 1 2 3''** to detect  **PMT**, **NDT** and **PTO** test smells from ''fastjson'' project.

Similarly, you can input ***''main_detector.py -project functionaljava -test_smell_types 4''** to detect **POW** test smells from ''functionaljava'' project.