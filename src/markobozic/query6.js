function (doc) {
  if (doc.highway.highwayid == 3) {
    emit(doc.station.stationid, {"name": doc.locationtext, "downstream": doc.station.downstream});
  }
}
