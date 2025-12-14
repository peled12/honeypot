import "./App.css";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getEvents } from "./api/events";
import Chart from "./components/Chart";
import useSocket from "./hooks/useSocket";

// TODO: implement filtering and maybe more
// TODO: improve ux

const EVENTS_QUERY_KEY = "events";

function App() {
  const queryClient = useQueryClient();

  const {
    data: events,
    refetch,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: [EVENTS_QUERY_KEY],
    queryFn: getEvents,
  });

  // handle coming socket events
  useSocket((newEvent) => {
    console.log(newEvent);

    // append new event to the existing data
    queryClient.setQueryData([EVENTS_QUERY_KEY], (oldData = []) => [
      ...oldData,
      newEvent,
    ]);
  });

  if (isLoading) return <p>Loading events...</p>;
  if (isError)
    return (
      <>
        <p>Error: {error.message}</p>
        <button onClick={refetch}>Refetch</button>
      </>
    );

  return (
    <div className="App">
      <Chart events={events} />
    </div>
  );
}

export default App;
