require([__awesome_qr_base_path + '/awesome-qr.min.js'], function (AwesomeQR) {
    var img = new Image();
    img.crossOrigin = "Anonymous";
    img.onload = () => {
        AwesomeQR.create({
            text: student_check_link,
            size: 800,
            dotScale: 0.35,
            correctLevel: 2,
            backgroundImage: img,
            backgroundDimming: 'rgba(0,0,0,0.1)',
            autoColor: true,
            bindElement: 'qrcode'
        });
    };
    img.src = logo_img;
});
document.addEventListener('DOMContentLoaded', () => {
    $('#qrcode').on('click', () => {
        window.open(student_check_link);
    });
});

var chatSocket = new WebSocket(ws_link);

chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    let message = data['message'];
    let student_id = message.student_id;
    let progressbar_value = Number(document.querySelector('[role="progressbar"]').getAttribute('aria-valuenow'));
    let progressbar_maxvalue = document.querySelector('[role="progressbar"]').getAttribute('aria-valuemax');
    if (message.status === 'approved') {
        document.querySelector("tr[data-user='"+ student_id + "'] img").src = link_img_ok;
        progressbar_value += 1;
    }
    else if (message.status === 'unapproved'){
        document.querySelector("tr[data-user='"+ student_id + "'] img").src = link_img_cancel;
        progressbar_value -= 1;
    }
    document.querySelector('[role="progressbar"]').setAttribute('aria-valuenow', progressbar_value);
    document.querySelector('[role="progressbar"]').style.width = (progressbar_value/progressbar_maxvalue)*100 +'%';
    document.querySelector('.progress .progress-bar-text').innerText = progressbar_value + ' из ' + progressbar_maxvalue;
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};