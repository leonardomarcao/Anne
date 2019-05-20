if(event.payload == 'x'){
    event.data = 0;
    app.publish('anne/count', 0, false, 0);
}else{
    if(event.topic == 'anne/padlock'){
        if (!event.data) event.data = 1;
        v = parseInt(event.data);
        app.openUri('http://www.mqttaps.ga?id='+payload);
        if(event.payload > 0){   
            event.data = parseInt(v+1); 
            app.publish('anne/padlock', 'i', false, 0);   
            app.publish('anne/count', v, false, 0);
        }
    }
}

