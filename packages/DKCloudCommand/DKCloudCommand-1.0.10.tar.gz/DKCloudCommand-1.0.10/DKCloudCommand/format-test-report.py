from xml.dom.minidom import parse
from jinja2 import Template


TEMPLATE="""
<html>
	<head>
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
		<style>
			ul li.error {
				color: red;
			}
			ul li.ok {
				color: black;
			}
			ul li.test-method {
				cursor: pointer;
			}
		</style>
		<script>
			function showTestInfo(e) {
				var testBody = $(e.target).find('testcase');
				var failureType = testBody.find('failure');
				var message = testBody.find('message');
			}
			$(document).ready(function(){
				$('li.test-method').click(showTestInfo);
				$('li.test-class').click(function(e){ $(e.target).find('ul').toggle(); });
			});
		</script>
	</head>
	<body>
		<div class="header">
			<h1>Test Suite {{suite_name}}, 
				Tests: {{test_count}}, 
				Errors:{{error_count}}, 
				Failures:{{failure_count}}, 
				Skip:{{skip_count}},
				Total Time:{{total_time}} s.</h1>
		</div>
		<div class="left" id="left">
			<ul>
			{% for test_class in test_classes %}
			<li class="test-class {{test_class.el_class}}">{{test_class.name}} ({{test_class.time}} s)
				<ul style="display:none;">
					{% for test_method in test_class.tests %}
						<li class="test-method {{test_method.el_class}}">{{test_method.name}}</li>
					{% endfor %}
				</ul>
			</li>
			{% endfor %}
		</div>
		<div class="center" id="center">
		</div>
	</body>
</html>
"""

class FailureNode:
	def __init__(self,node):
		self.node = node
		self.failure_type = node.getAttribute('type')
		self.message = node.getAttribute('message')

class ErrorNode:
	def __init__(self,node):
		self.node = node

class TestMethod:
	def __init__(self,node):
		self.name = node.getAttribute('name')
		failures = node.getElementsByTagName('failure')
		errors = node.getElementsByTagName('error')
		self.time = float(node.getAttribute('time'))
		outputs = node.getElementsByTagName('system-out')
		if len(outputs) > 0:
			self.output = outputs[0].firstChild.nodeValue
		else:
			self.output = ''

		if len(failures) > 0:
			self.failure = FailureNode(failures[0])
		else:
			self.failure = None

		if len(errors) > 0:
			self.error = ErrorNode(errors[0])
		else:
			self.error = None

		self.el_class = 'error' if self.error or self.failure else 'ok'

class TestCase:
	def __init__(self,name,nodes):
		self.name = name
		self.tests = []
		self.failures = 0
		self.errors = 0
		self.skips = 0

		self.tests = [TestMethod(n) for n in nodes]
		self.failures = len([t for t in self.tests if t.failure])
		self.errors = len([t for t in self.tests if t.error])
		self.time = sum([t.time for t in self.tests])
		self.el_class = 'error' if self.failures > 0 else 'ok'

def get_test_e_class(node):
	failures = node.getElementsByTagName('failure')
	if len(failures) >0:
		return 'error'
	return 'ok'

def group_by_class(nodes):
	by_class = {}

	for node in nodes:
		class_name = node.getAttribute('classname')
		
		tests = []

		if class_name in by_class:
			tests = by_class[class_name]
		else:
			by_class[class_name] = tests

		tests.append(node)

	return [TestCase(k,v) for k,v in by_class.items()]

if __name__ == '__main__':
	dom = parse('test-results.xml')

	root = dom.documentElement

	test_nodes = root.getElementsByTagName('testcase')

	tests_by_class = group_by_class(test_nodes)
		
	template = Template(TEMPLATE)
		
	vars = {
		'suite_name': root.getAttribute('name'),
		'test_classes': tests_by_class,
		'failure_count': sum([t.failures for t in tests_by_class]),
		'error_count': sum([t.errors for t in tests_by_class]),
		'test_count': sum([len(t.tests) for t in tests_by_class]),
		'total_time': sum([t.time for t in tests_by_class])
	}
	output = template.render(vars)

with open('test-results.html','w') as f:
	f.write(output)


