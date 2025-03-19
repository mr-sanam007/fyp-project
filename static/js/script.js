// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if




    
}); 
// jquery end

// login registration logic

$(document).ready(function() {
    // Dropdown click fix
    $(document).on('click', '.dropdown-menu', function(e) {
        e.stopPropagation();
    });

    // Radio button logic
    $('.js-check :radio').change(function() {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name=' + check_attr_name + ']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
        } else {
            $(this).closest('.js-check').removeClass('active');
        }
    });

    // Checkbox logic
    $('.js-check :checkbox').change(function() {
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
        } else {
            $(this).closest('.js-check').removeClass('active');
        }
    });

    // Tooltip
    if ($('[data-toggle="tooltip"]').length > 0) {
        $('[data-toggle="tooltip"]').tooltip();
    }

    // --- Province and City logic ---
    const citiesByProvince = {
        "Kathmandu Valley": ["Kathmandu", "Bhaktapur", "Lalitpur"],
        "Province No. 1": ["Biratnagar", "Dharan", "Birtamode"],
        "Province No. 2": ["Janakpur", "Birgunj", "Rajbiraj"],
        "Bagmati Province": ["Hetauda", "Chandragiri", "Dhulikhel"],
        "Karnali Province": ["Surkhet", "Nepalgunj", "Jajarkot"],
        "Gandaki Province": ["Pokhara", "Bandipur", "Damauli"],
        "Lumbini Province": ["Butwal", "Tansen", "Lumbini"],
        "Sudurpashchim Province": ["Dhangadhi", "Mahendranagar", "Attariya"]
    };

    $('#inputProvince').on('change', function() {
        const province = $(this).val();
        const citySelect = $('#inputCity');
        citySelect.empty();

        if (province && citiesByProvince[province]) {
            citiesByProvince[province].forEach(city => {
                citySelect.append(`<option value="${city}">${city}</option>`);
            });
        } else {
            citySelect.append('<option value="">Choose a province first</option>');
        }
    });

    // --- Password toggle ---
    $('.toggle-password').on('click', function() {
        const input = $($(this).attr('toggle'));
        const type = input.attr('type') === 'password' ? 'text' : 'password';
        input.attr('type', type);
        $(this).toggleClass('fa-eye fa-eye-slash');
    });

});
