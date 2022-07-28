// Copyright (c) 2022, Accurate Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Chatbot Settings', {
	onload: function(frm) {

	},
	genrate:function(frm){
		frm.call("genrate").then(r => {
			var typeNumber = 0;
			var errorCorrectionLevel = 'L';
			var qr = accurate.utils.qrcode(typeNumber, errorCorrectionLevel);
			qr.addData(cur_frm.doc.token);
			qr.make();
			document.getElementById('qr').innerHTML = qr.createImgTag();
		});
	},disconnect:function(frm){
		frm.call("disconnect");
	}
});
