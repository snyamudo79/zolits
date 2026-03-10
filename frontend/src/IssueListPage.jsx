import React, { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import api from "./api";

function rowClass(issue) {
  const statusName = issue.status_name?.toUpperCase?.() || "";
  const severityName = issue.severity_name?.toUpperCase?.() || "";

  if (issue.status_is_resolved_state) {
    return "row-resolved";
  }
  if (severityName === "CRITICAL") {
    return "row-critical";
  }
  if (statusName === "PENDING") {
    return "row-pending";
  }
  return "";
}

function screenshotCell(issue) {
  const first = issue.attachments?.[0];
  if (!first?.file) return "";
  return (
    <a href={first.file} target="_blank" rel="noreferrer">
      View
    </a>
  );
}

export default function IssueListPage() {
  const [issues, setIssues] = useState([]);
  const [statuses, setStatuses] = useState([]);
  const [selectedIssue, setSelectedIssue] = useState(null);
  const [resolutionNotes, setResolutionNotes] = useState("");
  const [newStatus, setNewStatus] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/issues/")
      .then((res) => setIssues(res.data))
      .catch(() => setIssues([]));

    api.get("/statuses/").then((res) => setStatuses(res.data)).catch(() => setStatuses([]));
  }, []);

  const statusOptions = useMemo(() => statuses, [statuses]);

  const openIssue = (issue) => {
    setSelectedIssue(issue);
    setResolutionNotes(issue.resolution_notes || "");
    setNewStatus("");
    setError("");
  };

  const closeModal = () => {
    setSelectedIssue(null);
    setSaving(false);
    setError("");
  };

  const refreshIssues = async () => {
    const res = await api.get("/issues/");
    setIssues(res.data);
  };

  const saveUpdate = async () => {
    if (!selectedIssue) return;
    setSaving(true);
    setError("");
    try {
      const payload = {};
      if (newStatus) payload.status = Number(newStatus);
      payload.resolution_notes = resolutionNotes;
      await api.patch(`/issues/${selectedIssue.id}/`, payload);
      await refreshIssues();
      closeModal();
    } catch (e) {
      setError("Failed to update issue");
      setSaving(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Issues</h1>
        <Link to="/issues/new" className="primary">
          New Issue
        </Link>
      </div>
      <div className="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Description</th>
              <th>Region</th>
              <th>Depot</th>
              <th>Module</th>
              <th>Severity</th>
              <th>Status</th>
              <th>Raised</th>
              <th>Resolved By</th>
              <th>Date Resolved</th>
              <th>User</th>
              <th>Resolution</th>
              <th>Screenshot</th>
            </tr>
          </thead>
          <tbody>
            {issues.map((issue) => (
              <tr
                key={issue.id}
                className={rowClass(issue)}
                onClick={() => openIssue(issue)}
                style={{ cursor: "pointer" }}
              >
                <td>{issue.issue_number}</td>
                <td title={issue.description}>{issue.description?.slice(0, 40)}{issue.description && issue.description.length > 40 ? "…" : ""}</td>
                <td>{issue.region_name}</td>
                <td>{issue.depot_name}</td>
                <td>{issue.module_name}</td>
                <td>{issue.severity_name}</td>
                <td>{issue.status_name}</td>
                <td>{new Date(issue.date_issue_raised).toLocaleString()}</td>
                <td>{issue.resolved_by_name}</td>
                <td>{issue.date_issue_resolved ? new Date(issue.date_issue_resolved).toLocaleString() : ""}</td>
                <td>{issue.issue_logged_by_name}</td>
                <td title={issue.resolution_notes}>{issue.resolution_notes?.slice(0, 30)}{issue.resolution_notes && issue.resolution_notes.length > 30 ? "…" : ""}</td>
                <td>{screenshotCell(issue)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selectedIssue && (
        <div className="modal-backdrop" onClick={closeModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedIssue.issue_number}</h2>
              <button className="link-button" onClick={closeModal}>
                Close
              </button>
            </div>

            <div className="modal-body">
              <div className="kv">
                <div><strong>Region</strong><div>{selectedIssue.region_name}</div></div>
                <div><strong>Depot</strong><div>{selectedIssue.depot_name}</div></div>
                <div><strong>Module</strong><div>{selectedIssue.module_name}</div></div>
                <div><strong>Severity</strong><div>{selectedIssue.severity_name}</div></div>
                <div><strong>Status</strong><div>{selectedIssue.status_name}</div></div>
              </div>

              <div className="section">
                <strong>Description</strong>
                <div className="pre">{selectedIssue.description}</div>
              </div>

              <div className="section">
                <label>
                  New Status
                  <select value={newStatus} onChange={(e) => setNewStatus(e.target.value)}>
                    <option value="">(no change)</option>
                    {statusOptions.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.name}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="section">
                <label>
                  Resolution
                  <textarea value={resolutionNotes} onChange={(e) => setResolutionNotes(e.target.value)} />
                </label>
              </div>

              {selectedIssue.attachments?.length > 0 && (
                <div className="section">
                  <strong>Screenshots</strong>
                  <ul>
                    {selectedIssue.attachments.map((a) => (
                      <li key={a.id}>
                        <a href={a.file} target="_blank" rel="noreferrer">
                          View attachment {a.id}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {error && <div className="error">{error}</div>}
            </div>

            <div className="modal-actions">
              <button className="primary" onClick={saveUpdate} disabled={saving}>
                {saving ? "Saving…" : "Save"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

