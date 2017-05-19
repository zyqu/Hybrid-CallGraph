# Hybrid-CallGraph
Merge the callgraphs generated from:
  Dynamic Analysis https://github.com/zyqu/Dynamic-CallGraph-Generator-Android
  Static Analysis https://github.com/zyqu/FlowDroid-CallGraph

The output is the complete call graph. 
Copy the output from dynamic analysis (in dir "out/packageName") and the output from static analysis static-cfg-[APKFileName]

>> python merge.py path-to-static-analysis-result-file path-to-dynamic-analysis-result-dir
