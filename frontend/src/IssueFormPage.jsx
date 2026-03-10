import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api";

export default function IssueFormPage() {
  const [regions, setRegions] = useState([]);
  const [depots, setDepots] = useState([]);
  const [modules, setModules] = useState([]);
  const [severities, setSeverities] = useState([]);
  const [statuses, setStatuses] = useState([]);

  const [form, setForm] = useState({
    region: "",
    depot: "",
    module: "",
    functionality: "",
    description: "",
    raised_by_name: "",
    contact_phone: "",
    assigned_to: "",
    severity: "",
    status: ""
  });

  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [screenshot, setScreenshot] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    Promise.all([
      api.get("/regions/"),
      api.get("/depots/"),
      api.get("/modules/"),
      api.get("/severities/"),
      api.get("/statuses/"),
      api.get("/users/").catch(() => ({ data: [] }))
    ])
      .then(([r, d, m, sev, stat, u]) => {
        setRegions(r.data);
        setDepots(d.data);
        setModules(m.data);
        setSeverities(sev.data);
        setStatuses(stat.data);
        setUsers(u.data);
      })
      .catch(() => setError("Failed to load reference data"));
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const created = await api.post("/issues/", form);
      const issueId = created.data?.id;

      if (issueId && screenshot) {
        const fd = new FormData();
        fd.append("file", screenshot);
        await api.post(`/issues/${issueId}/attachments/`, fd, {
          headers: { "Content-Type": "multipart/form-data" }
        });
      }
      navigate("/issues");
    } catch (err) {
      setError("Failed to create issue");
    }
  };

  const filteredDepots = depots.filter((d) => d.region.id === Number(form.region));

  return (
    <div>
      <h1>New Issue</h1>
      {error && <div className="error">{error}</div>}
      <form className="grid-form" onSubmit={handleSubmit}>
        <label>
          Region
          <select name="region" value={form.region} onChange={handleChange} required>
            <option value="">Select region</option>
            {regions.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Depot
          <select name="depot" value={form.depot} onChange={handleChange} required>
            <option value="">Select depot</option>
            {filteredDepots.map((d) => (
              <option key={d.id} value={d.id}>
                {d.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Module
          <select name="module" value={form.module} onChange={handleChange} required>
            <option value="">Select module</option>
            {modules.map((m) => (
              <option key={m.id} value={m.id}>
                {m.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Severity
          <select name="severity" value={form.severity} onChange={handleChange} required>
            <option value="">Select severity</option>
            {severities.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Status
          <select name="status" value={form.status} onChange={handleChange} required>
            <option value="">Select status</option>
            {statuses.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Assigned Expert
          <select name="assigned_to" value={form.assigned_to} onChange={handleChange}>
            <option value="">Select expert</option>
            {users.map((u) => (
              <option key={u.id} value={u.id}>
                {u.full_name || u.username}
              </option>
            ))}
          </select>
        </label>
        <label className="full-width">
          Functionality
          <input name="functionality" value={form.functionality} onChange={handleChange} required />
        </label>
        <label className="full-width">
          Issue Description
          <textarea name="description" value={form.description} onChange={handleChange} required />
        </label>
        <label className="full-width">
          Screenshot (optional)
          <input
            type="file"
            accept="image/*"
            onChange={(e) => setScreenshot(e.target.files?.[0] || null)}
          />
        </label>
        <label>
          Issue Raised By
          <input name="raised_by_name" value={form.raised_by_name} onChange={handleChange} required />
        </label>
        <label>
          Contact Phone
          <input name="contact_phone" value={form.contact_phone} onChange={handleChange} />
        </label>
        <div className="full-width actions">
          <button type="submit" className="primary">
            Submit
          </button>
        </div>
      </form>
    </div>
  );
}

