import Event from "../models/Event";

// formats values for display in the chart
function formatValue(val) {
  if (val === null || val === undefined) return "";
  if (val instanceof Date) return val.toLocaleString();
  if (typeof val === "boolean") return val ? "Yes" : "No";
  return String(val);
}

function Chart({ events = null }) {
  if (!events || !Array.isArray(events) || !events.length) {
    return <h1>No Data</h1>;
  }

  const rows = events;

  return (
    <div className="chart-component">
      <h1>Events Chart</h1>
      <table>
        <thead>
          <tr>
            {Event.fields.map((a) => (
              <th key={a}>{a}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((e, i) => (
            <tr key={i} style={{ borderBottom: "1px solid #eee" }}>
              {Event.fields.map((a) => (
                <td
                  key={a}
                  style={{
                    padding: "8px",
                    verticalAlign: "top",
                    border: "1px solid #f0f0f0",
                  }}
                >
                  {formatValue(e[a])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Chart;
