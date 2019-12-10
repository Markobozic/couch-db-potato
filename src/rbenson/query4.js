//Map Function
function (doc) {
    if (doc.docType == "loop" && doc.speed > 0 && doc.locationtext == "Sunnyside NB" && doc.starttime >= "2011-09-15 00:01:40-07" && doc.starttime <= "2011-09-15 00:08:40-07") {
        emit(doc.starttime, { "station_length": doc.length, "total_speed": doc.speed });
    }
}

//Reduce Function
function (keys, values, rereduce) {
    var result = { "TravelTime": 0, "travel_units": "seconds", "station_length": 0, "total_speed": 0, "avg_speed": 0 };

    for (var i = 0; i < values.length; ++i) {
        result.total_speed += values[i].total_speed;
        result.station_length = values[i].station_length;
    }

    result.avg_speed = result.total_speed / values.length;
    result.TravelTime = ((result.station_length / result.avg_speed) * 3660);

    return result;
}