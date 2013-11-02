cap = {
    validate: function(form) {
	$(form).validate({
	    rules: {
		target_ltv: {
		    required: true,
		    range: [99, 100]
		}
	    },
	    showErrors: function(errorMap, errorList) {
		$.each(this.successList, function(index, value) {
		    return $(value).popover("hide");
		});
		return $.each(errorList, function(index, value) {
		    var _popover;
		    _popover = $(value.element).popover({
			trigger: "manual",
			placement: "top",
			content: value.message,
			template: "<div class=\"popover\"><div class=\"arrow\"></div><div class=\"popover-inner\"><div class=\"popover-content\"><p></p></div></div></div>"
		    });
		    _popover.data("bs.popover").options.content = value.message;
		    return $(value.element).popover("show");
		});
	    }
	});
    }
};


