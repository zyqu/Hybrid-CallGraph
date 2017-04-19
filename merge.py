#!/usr/bin/python

import json, os, sys

def smaliType(s):
	s = s.strip()
	if s.endswith("[]"):
		return "[%s"%smaliType(s[:len(s) - 2])
	else:
		if s == "void":
			return "V"
		elif s == "boolean":
			return "Z"
		elif s == "byte":
			return "B"
		elif s == "short":
			return "S"
		elif s == "char":
			return "C"
		elif s == "int":
			return "I"
		elif s == "long":
			return "J"
		elif s == "float":
			return "F"
		elif s == "double":
			return "D"
		else:
			return "L%s;"%(s.replace(".", "/"))

def smaliSignature(sig):
	sig = sig.strip()

	if sig.startswith("<"):
		sig = sig[1:]

	if sig.endswith(">"):
		sig = sig[:len(sig) - 1]

	tokens = sig.split(" ")
	className = tokens[0]
	if className.endswith(":"):
		className = className[:len(className) - 1]
	className = className.strip()

	returnType = tokens[1]
	
	subTokens = tokens[2].split("(")
	
	methodName = subTokens[0]
	methodName = methodName.strip()
	
	paraTypes = subTokens[1]
	paraTypes = paraTypes[:len(paraTypes) - 1]
	paraTypes = paraTypes.split(",")

	smaliParaTypes = []
	for para in paraTypes:
		smaliParaTypes.append(smaliType(para))

	res = "%s.%s (%s)%s"%(className, methodName, ''.join(smaliParaTypes),smaliType(returnType))
	#print "%s -> %s"%(sig, res)
	return res


def graphParse2smali(origGraph):
	newGraph = {}
	for key in origGraph:
		valSet = origGraph[key]
		newSet = set()
		for val in valSet:
			newSet.add(smaliSignature(val))
		newGraph[smaliSignature(key)] = newSet
	return newGraph

if __name__=="__main__":
	if len(sys.argv) != 3:
		print "python merge.py path-to-static-call-graph path-to-dynamic-call-graph"
		sys.exit(-1)
	else:
		staticCGPath = sys.argv[1]
		dynamicCGPath = sys.argv[2]

		outputpath = "hybrid-cfg-%s"%(staticCGPath.replace("static-cfg-", ""))

		if not os.path.exists(staticCGPath):
			print "File not exist: %s"%staticCGPath
			sys.exit(-1)

		with open(staticCGPath, 'r') as fobj:
			staticCG = graphParse2smali(json.loads(fobj.read()))
			