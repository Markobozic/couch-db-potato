//map
function(doc) {
    if (doc.docType == "loop") {
      if(Number(doc.speed) !=0 && doc.locationtext == 'Foster NB'){
        if(doc.length) {
        
          year = Number(doc.starttime.substring(0,4));
          month = Number(doc.starttime.substring(5,7));
          day = Number(doc.starttime.substring(8,10));
          hour = Number(doc.starttime.substring(11,13));
          minute = Number(doc.starttime.substring(14,16));
          
          if(year == 2011 && month == 9 && day ==15) {
            emit(Math.floor(minute/5)*5, (doc.length/doc.speed)*3600);
          }
        }
      }
    }
}

//reduce
function(keys, values, rereduce) {
    if (!rereduce) {
        var length = values.length
        return [sum(values) / length, length]
    } else {
        var length = sum(values.map(function(v){return v[1]}));
        var avg = sum(values.map(function(v){
            return v[0] * (v[1] / length)
        }));
        return [avg, length]
    }
}

