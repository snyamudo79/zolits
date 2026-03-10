import React, { useEffect, useState } from "react";
import api from "./api";

export default function DashboardPage() {
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    api
      .get("/issues/")
      .then((res) => {
        const data = res.data;
        const total = data.length;
        const statusCounts = {};
        const severityCounts = {};
        data.forEach((i) => {
          statusCounts[i.status_name] = (statusCounts[i.status_name] || 0) + 1;
          severityCounts[i.severity_name] = (severityCounts[i.severity_name] || 0) + 1;
        });
        setSummary({ total, statusCounts, severityCounts });
      })
      .catch(() => setSummary(null));
  }, []);

  if (!summary) {
    return <div>Loading dashboard…</div>;
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="cards">
        <div className="card">
          <h2>Total issues</h2>
          <p className="big">{summary.total}</p>
        </div>
        <div className="card">
          <h2>By status</h2>
          <ul>
            {Object.entries(summary.statusCounts).map(([k, v]) => (
              <li key={k}>
                {k}: {v}
              </li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h2>By severity</h2>
          <ul>
            {Object.entries(summary.severityCounts).map(([k, v]) => (
              <li key={k}>
                {k}: {v}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

