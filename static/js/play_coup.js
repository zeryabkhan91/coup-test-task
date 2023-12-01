$(document).ready(function(){
    loadState();
});

window.reload = function(data){
    const location = window.location
    window.location.href = `${location.origin}/${data.url}`
}

function loadState() {
    window.setTimeout(function(){
        $.ajax({
            url: '/long_polling',
            method: 'GET',
            dataType: 'json',
            success: function(event){
                if(event != {})
                {
                    if (window[event.type]) 
                        window[event.type](event.data);
                    if(event.data && event.data.ai_turn) {  ai_turn() }

                    loadState();
                }
            }
        });
    }, 2000);
}

function ai_turn() {
    $.ajax({
        url: '/ai-turn',
        method: 'GET',
        error: function(xhr, status, error) {
            console.error("Failed to trigger AI turn:", status, error);
        }
    });
}

function verifyAmbassador(){
{
    var n_cards = $("#n_cards");
    if (n_cards == null){
        console.log('Not ambassador');
        return 0
    } else {
        var checkboxes = $("[name=selected_cards]");
        var numberOfCheckedItems = 0;
        for(var i = 0; i < checkboxes.length; i++)
        {
            if(checkboxes[i].checked)
                numberOfCheckedItems++;
        }
        if (numberOfCheckedItems != 2)
        {
            alert('You selected not ' + n_cards + ' cards!');
            return -1
        }
    };
    return 1
}
};

