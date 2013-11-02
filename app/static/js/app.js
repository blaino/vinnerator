cap = {
    setupValidation: function() {
	$.validator.addClassRules({
	    percentage: {
		required: true,
		range: [0, 100]
	    },
	    number: {
		required: true,
		min: 0
	    },
	    scenario: {
		required: true,
		maxlength: 30
	    }
	});
    },
    validate: function(form) {
	$(form).validate({
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


