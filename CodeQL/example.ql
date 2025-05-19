
import python

from Call call, Attribute attr
where
    attr = call.getFunc() and
    (attr.getName() = "loads" or attr.getName() = "load") and 
    not call.getEnclosingModule().getName().matches("%test%")

select attr.getObject(), attr.getName(), call.getLocation()

