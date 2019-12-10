function(doc) {
  if (doc.speed.length > 2 && doc.speed !== '100') {
    emit(doc.speed, 1)
  }
}

function(keys, values, rereduce) {
  return _count(values)
}
