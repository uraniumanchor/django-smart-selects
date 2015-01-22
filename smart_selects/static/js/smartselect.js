function generateSmartSelect($,chainfield,url,id,value,auto_choose,empty_label) {
	function fireEvent(element,event) {
		if (document.createEventObject) {
			// dispatch for IE
			var evt = document.createEventObject();
			return element.fireEvent('on'+event,evt)
		} else {
			// dispatch for firefox + others
			var evt = document.createEvent("HTMLEvents");
			evt.initEvent(event, true, true ); // event type,bubbling,cancelable
			return !element.dispatchEvent(evt);
		}
	}

	function dismissRelatedLookupPopup(win, chosenId) {
		var name = windowname_to_id(win.name);
		var elem = document.getElementById(name);
		if (elem.className.indexOf('vManyToManyRawIdAdminField') != -1 && elem.value) {
			elem.value += ',' + chosenId;
		} else {
			elem.value = chosenId;
		}
		fireEvent(elem, 'change');
		win.close();
	}

	$(document).ready(function(){
		function fill_field(val, init_value){
			if (!val || val==''){
				options = '<option value="">'+empty_label+'</option>';
				$('#'+id).html(options);
				$('#'+id+' option:first').attr('selected', 'selected');
				$('#'+id).trigger('change');
				return;
			}
			$.getJSON(url+'/'+val+'/', function(j){
				var options = '<option value="">'+empty_label+'</option>';
				for (var i = 0; i < j.length; i++) {
					options += '<option value="' + j[i].value + '">' + j[i].display + '<'+'/option>';
				}
				var width = $('#'+id).outerWidth();
				$('#'+id).html(options);
				if (navigator.appVersion.indexOf("MSIE") != -1)
					$('#'+id).width(width + 'px');
				$('#'+id+' option:first').attr('selected', 'selected');
				if(init_value){
					$('#'+id+' option[value="'+ init_value +'"]').attr('selected', 'selected');
				}
				if(auto_choose && j.length == 1){
					$('#'+id+' option[value="'+ j[0].value +'"]').attr('selected', 'selected');
				}
				$('#'+id).trigger('change');
			})
		}

		if(!$('#id_'+chainfield).hasClass("chained")){
			var val = $('#id_'+chainfield).val();
			fill_field(val, value);
		}

		$('#id_'+chainfield).change(function(){
			var start_value = $('#'+id).val();
			var val = $(this).val();
			fill_field(val, start_value);
		})
	})
	var oldDismissAddAnotherPopup = dismissAddAnotherPopup;
	dismissAddAnotherPopup = function(win, newId, newRepr) {
		oldDismissAddAnotherPopup(win, newId, newRepr);
		if (windowname_to_id(win.name) == 'id_'+chainfield) {
			$('id_'+chainfield).change();
		}
	}
}