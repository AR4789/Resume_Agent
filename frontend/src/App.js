import { useState } from "react";

function App() {
  const [resume, setResume] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [company, setCompany] = useState("");
  const [role, setRole] = useState("");
  const [applicantName, setApplicantName] = useState("");
  const [applyEmail, setApplyEmail] = useState("");
  const [resumeType, setResumeType] = useState("normal");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [linkedinStatus, setLinkedinStatus] = useState("");
  const [design, setDesign] = useState("modern");
  const [density, setDensity] = useState("detailed");


  const submit = async () => {
    setError("");
    setResult(null);

    if (!resume || !jobDescription || !company || !role || !applicantName) {
      setError("Please fill all required fields.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDescription);
    formData.append("company", company);
    formData.append("role", role);
    formData.append("applicant_name", applicantName);
    formData.append("resume_type", resumeType);
    formData.append("design", design);
    formData.append("density", density);
    if (applyEmail) formData.append("apply_email", applyEmail);

    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/optimize", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Server error while optimizing resume");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "#f9fafb", fontFamily: "Inter, system-ui, sans-serif" }}>
      <div style={{ maxWidth: 1000, margin: "0 auto", padding: 40 }}>
        <h1 style={{ fontSize: 34, fontWeight: 700 }}>AI Resume Agent</h1>
        <p style={{ color: "#555", marginBottom: 30 }}>
          Optimize your resume, analyze ATS score, and apply smarter.
        </p>

        {/* FORM */}
        <div
          style={{
            background: "#fff",
            padding: 30,
            borderRadius: 10,
            boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
          }}
        >
          <input type="file" accept=".pdf,.docx" onChange={(e) => setResume(e.target.files[0])} />

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 15, marginTop: 20 }}>
            <input placeholder="Applicant Name *" onChange={(e) => setApplicantName(e.target.value)} />
            <input placeholder="Target Company *" onChange={(e) => setCompany(e.target.value)} />
            <input placeholder="Target Role *" onChange={(e) => setRole(e.target.value)} />
            <input placeholder="Apply Email (optional)" onChange={(e) => setApplyEmail(e.target.value)} />
          </div>

          <select
            value={resumeType}
            onChange={(e) => setResumeType(e.target.value)}
            style={{ marginTop: 15, padding: 10, width: "100%", borderRadius: 6 }}
          >
            <option value="normal">Normal (Balanced)</option>
            <option value="faang">FAANG (Impact & Metrics)</option>
            <option value="startup">Startup (Ownership & Speed)</option>
          </select>

          <select
            value={design}
            onChange={(e) => setDesign(e.target.value)}
            style={{ marginTop: 15, padding: 10, width: "100%", borderRadius: 6 }}
          >
            <option value="minimal">Minimal</option>
            <option value="modern">Modern</option>
            <option value="premium">Premium</option>
          </select>

          <select
            value={density}
            onChange={(e) => setDensity(e.target.value)}
            style={{ marginTop: 10, padding: 10, width: "100%", borderRadius: 6 }}
          >
            <option value="compact">Compact</option>
            <option value="detailed">Detailed</option>
          </select>


          <textarea
            rows={6}
            placeholder="Paste Job Description *"
            style={{ width: "100%", marginTop: 15 }}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <button
            onClick={submit}
            disabled={loading}
            style={{
              marginTop: 20,
              padding: "12px 24px",
              background: "#2563eb",
              color: "#fff",
              border: "none",
              borderRadius: 6,
              fontSize: 16,
              cursor: "pointer",
            }}
          >
            {loading ? "Optimizing..." : "Optimize Resume"}
          </button>

          {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}
        </div>

        {/* RESULTS */}
        {result && (
          <div style={{ marginTop: 40 }}>
            <a
              href={`http://localhost:8000${result.resume_download_url}`}
              download
              style={{
                display: "inline-block",
                marginTop: 15,
                padding: "10px 20px",
                background: "#16a34a",
                color: "#fff",
                textDecoration: "none",
                borderRadius: 6,
                fontWeight: 600,
              }}
            >
              ⬇ Download Optimized Resume
            </a>

            <h2>Results</h2>

            <p><strong>ATS Score:</strong> {result.ats.ats_score}%</p>
            <p><strong>Auto Applied:</strong> {result.applied ? "Yes" : "No"}</p>

            {/* ✅ EMAIL ERROR (FIXED) */}
            {result.email_error && (
              <p style={{ color: "#dc2626", marginTop: 8 }}>
                {result.email_error}
              </p>
            )}

            {/* ATS BAR */}
            <div style={{ marginTop: 20 }}>
              <div style={{ background: "#e5e7eb", height: 12, borderRadius: 6 }}>
                <div
                  style={{
                    width: `${result.ats.ats_score}%`,
                    background: result.ats.ats_score > 70 ? "#16a34a" : "#dc2626",
                    height: "100%",
                  }}
                />
              </div>
            </div>

            {/* MISSING KEYWORDS */}
            {result.ats.missing_keywords?.length > 0 && (
              <div style={{ marginTop: 20 }}>
                <h3>Missing Keywords</h3>
                <ul>
                  {result.ats.missing_keywords.slice(0, 15).map((k) => (
                    <li key={k}>{k}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* LINKEDIN APPLY */}
            <div style={{ marginTop: 40 }}>
              <h3>Apply on LinkedIn</h3>

              <input
                placeholder="Paste LinkedIn Job URL"
                style={{ width: "100%", padding: 8 }}
                value={linkedinUrl}
                onChange={(e) => setLinkedinUrl(e.target.value)}
              />

              <button
                style={{
                  marginTop: 10,
                  padding: "10px 20px",
                  background: "#0a66c2",
                  color: "#fff",
                  border: "none",
                  borderRadius: 6,
                }}
                onClick={async () => {
                  setLinkedinStatus("Starting LinkedIn apply...");

                  const fd = new FormData();
                  fd.append("job_url", linkedinUrl);
                  fd.append("resume_file", result.resume_file);

                  const res = await fetch("http://localhost:8000/apply/linkedin", {
                    method: "POST",
                    body: fd,
                  });

                  const data = await res.json();
                  setLinkedinStatus(data.status);
                }}
              >
                Apply on LinkedIn
              </button>

              {linkedinStatus && <p>{linkedinStatus}</p>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
