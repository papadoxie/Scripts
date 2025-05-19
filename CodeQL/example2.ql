/**
 * @name User input reaching deserialization
 * @description Tracks user-controlled data flowing into deserialization functions
 * @kind path-problem
 * @problem.severity warning
 * @id py/user-input-marshal-deserialization
*/

import python
import semmle.python.dataflow.new.DataFlow
import semmle.python.dataflow.new.TaintTracking
import semmle.python.dataflow.new.RemoteFlowSources

 
module DeserializationFlow implements DataFlow::ConfigSig {
    predicate isSource(DataFlow::Node node) {
        node instanceof RemoteFlowSource or 
        exists (Call c, Attribute attr |
            c = node.asExpr() and
            (
                not c.getEnclosingModule().getName().matches("%test%") and
                attr = c.getFunc() 
            )
        )
    }

    predicate isSink(DataFlow::Node node) {
        exists (Call c, Attribute attr |
            c = node.asExpr() and
            (
                not c.getEnclosingModule().getName().matches("%test%") and
                attr = c.getFunc() and
                attr.getName() = "func_load"
                // attr.getObject().toString() = "marshal" 
                // and (attr.getName() = "loads" or attr.getName() = "load")
            )
        )
    }
}

module Flow = TaintTracking::Global<DeserializationFlow>;
import Flow::PathGraph

from Flow::PathNode source, Flow::PathNode sink, Attribute src, Attribute snk
where
    Flow::flowPath(source, sink)
    and source != sink
    and source.getNode().asExpr() instanceof Call
    and sink.getNode().asExpr() instanceof Call
    and src = ((Call)source.getNode().asExpr()).getFunc()
    and snk = ((Call)sink.getNode().asExpr()).getFunc()
select 
    sink.getNode().getEnclosingCallable(), source, sink, 
    "Found Path from " + 
    src.getObject().toString() + "." + src.getName() + 
    " to " + 
    snk.getObject().toString() + "." + snk.getName()


