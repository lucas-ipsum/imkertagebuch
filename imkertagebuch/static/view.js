// Allgemeiner Befund 
var wab_bel = {btn_up: '#wabenbelegt_plus', btn_down: '#wabenbelegt_minus', value_field: '#spinner_val_wabenbelegt', min: 0}
var futter = {btn_up: '#futter_plus', btn_down: '#futter_minus', value_field: '#spinner_val_futter', min:0}
// Hinzufuegen / Entnehmen 
var veraend_waben = {btn_up: '#waben_plus', btn_down: '#waben_minus', value_field: '#spinner_val_veraend_waben', min: -10}
var veraend_mittelwand = {btn_up: '#mittelwand_plus', btn_down: '#mittelwand_minus', value_field: '#spinner_val_veraend_mittelwand', min: -10}
var veraend_brut = {btn_up: '#brut_plus', btn_down: '#brut_minus', value_field: '#spinner_val_veraend_brut', min: -10}
var veraend_drohnenrahmen = {btn_up: '#drohnenrahmen_plus', btn_down: '#drohnenrahmen_minus', value_field: '#spinner_val_veraend_drohnenrahmen', min: -10}
var veraend_bienen = {btn_up: '#bienen_plus', btn_down: '#bienen_minus', value_field: '#spinner_val_veraend_bienen', min: -10}
var veraend_honig_kg = {btn_up: '#honig_plus', btn_down: '#honig_minus', value_field: '#spinner_val_veraend_honig_kg', min: -10}
// Slider
var position;
var wabensitz_liste = ['Links', 'Mitte-Links','Mitte', 'Mitte-Rechts', 'Rechts']

// Funktionsaufrufe (on startup)
init_Slider_Val();
create_Spinner_and_value();

$('.table > tbody > tr').click(function() {
    console.log(event)
    // TODO Stockeintrag id aus Tabelle auslesen + Link auf spezifischen Stockeintrag
});

// ####### Slider ######
// Slider -> Display initial values 
function init_Slider_Val() {
    var sanftmut = $('#sanftmut_slider').val()
    var position = $('#wabensitz_slider').val()
    $('#sanftmut_value').html(sanftmut);
    $('#wabensitz_value').html(wabensitz_liste[position]);
}

$(document).on('input', '#sanftmut_slider', function() {
    $('#sanftmut_value').html($(this).val());
});

$(document).on('input', '#wabensitz_slider', function() {
    position = $(this).val()
    $('#wabensitz_value').html(wabensitz_liste[position]);
});


// ##### Spinner #####
function create_Spinner_and_value() {
    init_Spinner(wab_bel);
    init_Spinner(futter);
    init_Spinner(veraend_bienen);
    init_Spinner(veraend_brut)
    init_Spinner(veraend_drohnenrahmen);
    init_Spinner(veraend_honig_kg);
    init_Spinner(veraend_mittelwand);
    init_Spinner(veraend_waben);
}

// Funktionalität Spinner Buttons
function init_Spinner(appObj) {
    var value = $(appObj.value_field).val();
    value = parseInt(value);
    // Plus Button 
    $(appObj.btn_up).on('mousedown', function() {
        value = value + 1; 
        $(appObj.value_field).val(value);
    });
    // Minus Button 
    $(appObj.btn_down).on('click', function() {
        if(value - 1 >= appObj.min) {
            value = value - 1; 
        }
        $(appObj.value_field).val(value);
    });
    // Text Change 
    $(appObj.value_field).on('input', function(){
        var txt_input = parseInt($(appObj.value_field).val());
        if(isNaN(txt_input) || txt_input < appObj.min || txt_input > appObj.max) {                                  // Falls keine Nummer eingegeben wird. Auf Null setzen 
            value = 0;                                                                     // TODO ggf. Alert mit Fehlerhinweis 
            //$(appObj.value_field).val(value)
        }
        else {
            value = txt_input;
        }
    }); 
}

// Expand StockEintrag
$('#expand_buttons').on('click', function() {
    var expanded = document.getElementById('expand_buttons').getAttribute('aria-expanded')
    console.log(expanded)
    if(expanded == 'true') {
        $('#arrow_down').hide();
        $('#arrow_up').show();
    }
    else {
        $('#arrow_down').show();
        $('#arrow_up').hide();
    }
});
