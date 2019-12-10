//Map Function
function (doc) {
  if(doc.docType == "loop" && doc.speed > 0 && doc.locationtext == "Foster NB" && doc.starttime >= "2011-09-22 16:00:00-07" && doc.starttime <= "2011-09-22 18:00:00-07" ) {
    emit(doc.starttime, {"station_length": doc.length, "total_speed": doc.speed, "count": 1});
  }
}

//Reduce Function
function(keys, values, rereduce) {
    var result = {
        'TravelTime': 0,
        'travel_units': 'seconds',
        'station_length': 0,
        'total_speed': 0,
        'avg_speed': 0,
        'count': 0,
    };
    for (var i = 0; i < values.length; ++i) {
        result.total_speed += values[i].total_speed;
        result.station_length = values[i].station_length;
        result.count += values[i].count;
    }
    result.avg_speed = result.total_speed / result.count;
    result.TravelTime = ((result.station_length / result.avg_speed) * 3660);
    return result;
}