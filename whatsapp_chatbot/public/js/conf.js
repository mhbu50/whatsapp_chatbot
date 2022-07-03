frappe.provide("accurate.utils");
accurate.utils.wait = function (ms) {
    var d = new Date();
    var d2 = null;
    do { d2 = new Date(); }
    while (d2 - d < ms);
  }
  