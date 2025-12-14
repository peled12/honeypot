import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL;

export async function getEvents() {
  const res = await axios.get(`${API_BASE_URL}/testing/get-events`);
  console.log(res.data);

  return res.data;
}

export async function addEvent(event) {
  const res = await axios.post(`${API_BASE_URL}/testing/add-event`, event);
  return res.data;
}
