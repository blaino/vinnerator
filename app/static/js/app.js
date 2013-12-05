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
	    },
	    yesno: {
		required: true,
		yesnoRegex: "^[YyNn].{0,2}$"
	    }
	});
	$.validator.addMethod(
            "yesnoRegex",
            function(value, element, regexp) {
		var re = new RegExp(regexp);
		return this.optional(element) || re.test(value);
            },
            "Please enter yes or no."
	);
    },
    validate: function(form) {
	$(form).validate({
	    showErrors: function(errorMap, errorList) {
		$.each(this.successList, function(index, value) {
		    return $(value).popover("hide");
		});
		return $.each(errorList, function(index, value) {
		    var _popover;
		    var placement = "top";
		    if (value.element.name == 'title') {
			placement = "bottom";
		    }
		    _popover = $(value.element).popover({
			trigger: "manual",
			placement: placement,
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


