class Event {
  static fields = [
    "timestamp",
    "src_ip",
    "src_port",
    "dest_port",
    "service",
    "action",
    "banner",
    "raw_payload",
    "full_path",
    "geo_country",
    "fingerprint",
    "notes",
  ];

  constructor({
    timestamp = new Date(),
    src_ip = "",
    src_port = null,
    dest_port = null,
    service = "",
    action = "",
    banner = "",
    raw_payload = "",
    full_path = "",
    geo_country = "",
    fingerprint = "",
    notes = "",
  } = {}) {
    this.timestamp = timestamp;
    this.src_ip = src_ip;
    this.src_port = src_port;
    this.dest_port = dest_port;
    this.service = service;
    this.action = action;
    this.banner = banner;
    this.raw_payload = raw_payload;
    this.full_path = full_path;
    this.geo_country = geo_country;
    this.fingerprint = fingerprint;
    this.notes = notes;
  }
}

export default Event;
