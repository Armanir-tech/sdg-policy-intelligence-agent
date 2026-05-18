import {
  ArrowRight,
  BookOpenText,
  CheckCircle2,
  FileSearch,
  Layers3,
  LineChart,
  Network,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { ChangeEvent, FormEvent, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles/app.css";

type Source = {
  title: string;
  location: string;
  excerpt: string;
};

type ResearchResponse = {
  question: string;
  answer: string;
  policy_brief: string;
  sources: Source[];
  validation_notes: string[];
  workflow_steps: string[];
};

type IndexedDocument = {
  file_name: string;
  title: string;
  chunks: number;
  source_type: string;
};

const exampleResponse: ResearchResponse = {
  question: "How can private sector finance support SDG implementation?",
  answer:
    "Private sector finance can support SDG implementation by expanding investment capacity, improving innovation diffusion, and helping governments close financing gaps when public budgets are constrained.",
  policy_brief:
    "Problem: SDG implementation often faces financing constraints.\n\nEvidence: Development finance literature highlights the role of blended finance, risk-sharing, and private capital mobilization.\n\nRecommendation: Build transparent financing mechanisms, define measurable impact targets, and monitor whether private participation improves inclusion rather than only increasing investment volume.",
  sources: [
    {
      title: "Sample development policy report",
      location: "Page 12",
      excerpt: "Blended finance can mobilize private capital when risk-sharing mechanisms are transparent.",
    },
    {
      title: "Sample SDG financing note",
      location: "Page 4",
      excerpt: "Impact measurement is essential for aligning private investment with development outcomes.",
    },
  ],
  validation_notes: ["2 supporting sources found", "Policy brief includes problem, evidence, and recommendation sections"],
  workflow_steps: ["research", "analysis", "validation", "brief"],
};

const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL || `${window.location.protocol}//${window.location.hostname}:8000`;

const workflowSteps: Array<{
  step: string;
  description: string;
  Icon: LucideIcon;
}> = [
  { step: "Retrieve", description: "Find matching report sections", Icon: FileSearch },
  { step: "Analyze", description: "Summarize the strongest evidence", Icon: LineChart },
  { step: "Validate", description: "Check source coverage", Icon: ShieldCheck },
  { step: "Brief", description: "Draft policy recommendation", Icon: BookOpenText },
];

function App() {
  const [question, setQuestion] = useState(exampleResponse.question);
  const [result, setResult] = useState<ResearchResponse>(exampleResponse);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("Sample reports are already indexed.");
  const [documents, setDocuments] = useState<IndexedDocument[]>([]);
  const [currentStage, setCurrentStage] = useState("Ready");
  const [activeTab, setActiveTab] = useState<"answer" | "brief" | "sources" | "validation">("answer");

  async function refreshDocuments() {
    try {
      const response = await fetch(`${apiBaseUrl}/documents`);
      if (!response.ok) {
        throw new Error("Failed to load documents");
      }
      const payload = await response.json();
      setDocuments(payload.documents);
    } catch {
      setDocuments([]);
    }
  }

  useEffect(() => {
    refreshDocuments();
  }, []);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setCurrentStage("Searching indexed documents");

    try {
      await new Promise((resolve) => window.setTimeout(resolve, 250));
      setCurrentStage("Retrieving evidence");
      const response = await fetch(`${apiBaseUrl}/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      setCurrentStage("Writing answer and brief");
      setResult(await response.json());
      setCurrentStage("Analysis complete");
    } catch {
      setResult({ ...exampleResponse, question });
      setCurrentStage("Fallback response shown");
    } finally {
      setLoading(false);
    }
  }

  async function handleUpload(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    setUploading(true);
    setUploadMessage(`Uploading ${file.name}`);
    setCurrentStage("Indexing uploaded document");

    try {
      const response = await fetch(`${apiBaseUrl}/documents/upload`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const payload = await response.json();
      setUploadMessage(`${payload.file_name} indexed with ${payload.chunks} chunks.`);
      await refreshDocuments();
      setQuestion(`What are the main findings and recommendations in ${payload.file_name}?`);
      setCurrentStage("Document indexed");
    } catch {
      setUploadMessage("Upload failed. Use a PDF or TXT file and try again.");
      setCurrentStage("Upload failed");
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="brandMark">S</span>
          <div>
            <strong>SDG Policy Intelligence</strong>
            <small>Research agent workspace</small>
          </div>
        </div>
        <nav className="navPills" aria-label="Workspace status">
          <span>Evidence retrieval</span>
          <span>Policy brief</span>
          <span>Validation</span>
        </nav>
      </header>

      <section className="workspace">
        <aside className="queryPanel">
          <div className="panelTitle">
            <Network size={18} />
            Research request
          </div>
          <h1>Ask a policy question and trace the evidence.</h1>
          <p>
            Search the report collection, inspect supporting passages, and turn findings
            into a structured policy brief.
          </p>

          <form className="questionBox" onSubmit={handleSubmit}>
            <label htmlFor="research-question">Question</label>
            <textarea
              id="research-question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              aria-label="Research question"
            />
            <button type="submit" disabled={loading}>
              {loading ? "Analyzing evidence" : "Run analysis"}
              <ArrowRight size={18} />
            </button>
          </form>

          <div className="metricStrip">
            <div>
              <strong>{documents.length}</strong>
              <span>documents</span>
            </div>
            <div>
              <strong>{result.sources.length}</strong>
              <span>sources</span>
            </div>
            <div>
              <strong>{loading || uploading ? "Busy" : "Ready"}</strong>
              <span>status</span>
            </div>
          </div>

          <div className="uploadPanel">
            <div>
              <strong>Add a report</strong>
              <span>{uploadMessage}</span>
            </div>
            <label className={uploading ? "uploadButton disabled" : "uploadButton"}>
              {uploading ? "Indexing" : "Upload PDF/TXT"}
              <input type="file" accept=".pdf,.txt" onChange={handleUpload} disabled={uploading} />
            </label>
          </div>

          <div className="documentsPanel">
            <div className="documentsHeader">
              <strong>Indexed documents</strong>
              <button type="button" onClick={refreshDocuments}>Refresh</button>
            </div>
            {documents.length === 0 ? (
              <p>No indexed documents found yet.</p>
            ) : (
              <div className="documentList">
                {documents.map((document) => (
                  <button
                    type="button"
                    className="documentItem"
                    key={document.file_name}
                    onClick={() =>
                      setQuestion(`What are the main findings and recommendations in ${document.file_name}?`)
                    }
                  >
                    <span>{document.title}</span>
                    <small>{document.file_name} · {document.chunks} chunks · {document.source_type}</small>
                  </button>
                ))}
              </div>
            )}
          </div>
        </aside>

        <section className="analysisPanel">
          <div className="workflowRail" aria-label="Workflow">
            {workflowSteps.map(({ step, description, Icon }, index) => (
              <div
                className={result.workflow_steps?.includes(step.toLowerCase()) ? "workflowStep complete" : "workflowStep"}
                key={step}
              >
                <span>{index + 1}</span>
                <div>
                  <strong>{step}</strong>
                  <p>{description}</p>
                </div>
                <Icon size={18} />
              </div>
            ))}
          </div>

          <div className="stageBanner">
            <span>{currentStage}</span>
            <p>
              Uploading adds documents to the evidence index. Running analysis searches those indexed documents and returns the strongest source passages.
            </p>
          </div>

          <article className="resultPanel">
            <div className="resultHeader">
              <div>
                <div className="sectionLabel">
                  <Layers3 size={18} />
                  Analysis result
                </div>
                <h2>{result.question}</h2>
              </div>
              <div className="qualityBadge">
                <Sparkles size={16} />
                Source-aware
              </div>
            </div>

            <div className="tabs" role="tablist" aria-label="Analysis sections">
              {[
                ["answer", "Answer"],
                ["brief", "Policy brief"],
                ["sources", "Sources"],
                ["validation", "Validation"],
              ].map(([id, label]) => (
                <button
                  key={id}
                  type="button"
                  className={activeTab === id ? "active" : ""}
                  onClick={() => setActiveTab(id as typeof activeTab)}
                >
                  {label}
                </button>
              ))}
            </div>

            <div className="tabContent">
              {activeTab === "answer" && (
                <div className="answerBlock">
                  <p>{result.answer}</p>
                </div>
              )}

              {activeTab === "brief" && (
                <div className="briefBlock">
                  {result.policy_brief.split("\n\n").map((section) => (
                    <p key={section}>{section}</p>
                  ))}
                </div>
              )}

              {activeTab === "sources" && (
                <div className="sources">
                  {result.sources.map((source, index) => (
                    <div className="sourceCard" key={`${source.title}-${source.location}`}>
                      <div className="sourceTopline">
                        <strong>{source.title}</strong>
                        <span>#{index + 1}</span>
                      </div>
                      <small>{source.location}</small>
                      <p>{source.excerpt}</p>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === "validation" && (
                <ul className="checkList">
                  {result.validation_notes.map((note) => (
                    <li key={note}>
                      <CheckCircle2 size={17} />
                      {note}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </article>
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
