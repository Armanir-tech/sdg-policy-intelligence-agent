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

type Language = "en" | "tr";
type TabId = "answer" | "brief" | "sources" | "validation";
type Provider = "auto" | "groq" | "gemini" | "openrouter";

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
  provider_used: string;
};

type IndexedDocument = {
  file_name: string;
  title: string;
  chunks: number;
  source_type: string;
};

const copy = {
  en: {
    workspace: "Research agent workspace",
    pills: ["Evidence retrieval", "Policy brief", "Validation"],
    panelTitle: "Research request",
    headline: "Ask a policy question and trace the evidence.",
    intro:
      "Search the report collection, inspect supporting passages, and turn findings into a structured policy brief.",
    questionLabel: "Question",
    analyzing: "Analyzing evidence",
    run: "Run analysis",
    documents: "documents",
    sources: "sources",
    status: "status",
    ready: "Ready",
    busy: "Busy",
    addReport: "Add a report",
    providerLabel: "AI provider",
    providerHelp: "Auto tries configured providers in order and falls back safely.",
    providers: {
      auto: "Auto",
      groq: "Groq",
      gemini: "Gemini",
      openrouter: "OpenRouter",
    },
    providerUsed: "provider",
    signalEvidence: "Evidence index",
    signalEvidenceText: "documents searchable",
    signalRouting: "AI routing",
    signalRoutingText: "selected provider",
    signalWorkflow: "Agent workflow",
    signalWorkflowText: "controlled steps",
    sampleIndexed: "Sample reports are already indexed.",
    upload: "Upload PDF/TXT",
    uploading: "Uploading",
    indexing: "Indexing",
    uploadFailed: "Upload failed. Use a PDF or TXT file and try again.",
    indexedDocuments: "Indexed library",
    indexedHelp: "Private upload names and excerpts are masked in the public demo.",
    refresh: "Refresh",
    noDocuments: "No indexed documents found yet.",
    chunk: "chunks",
    consoleTitle: "Live agent route",
    consoleText: "RAG search -> LLM reasoning -> policy brief",
    privacyTitle: "Privacy mode",
    privacyText: "Public viewers see masked upload labels only.",
    stageReady: "Ready",
    stageSearching: "Searching indexed documents",
    stageRetrieving: "Retrieving evidence",
    stageWriting: "Writing answer and brief",
    stageComplete: "Analysis complete",
    stageFallback: "Fallback response shown",
    stageIndexing: "Indexing uploaded document",
    stageIndexed: "Document indexed",
    stageUploadFailed: "Upload failed",
    stageHelp:
      "Uploading adds documents to the evidence index. Running analysis searches those indexed documents and returns the strongest source passages.",
    result: "Analysis result",
    sourceAware: "Source-aware",
    tabs: {
      answer: "Answer",
      brief: "Policy brief",
      sources: "Sources",
      validation: "Validation",
    },
    workflow: [
      { step: "Retrieve", description: "Find matching report sections", key: "research" },
      { step: "Analyze", description: "Summarize the strongest evidence", key: "analysis" },
      { step: "Validate", description: "Check source coverage", key: "validation" },
      { step: "Brief", description: "Draft policy recommendation", key: "brief" },
    ],
    exampleQuestion: "How can private sector finance support SDG implementation?",
    uploadedQuestion: () => "What are the main findings and recommendations in the uploaded document?",
    indexedMessage: (_fileName: string, chunks: number) => `Uploaded document indexed with ${chunks} chunks.`,
    uploadingMessage: (fileName: string) => `Uploading ${fileName}`,
  },
  tr: {
    workspace: "Araştırma ajanı çalışma alanı",
    pills: ["Kanıt arama", "Politika notu", "Doğrulama"],
    panelTitle: "Araştırma isteği",
    headline: "Politika sorunu sor, kanıtı adım adım izle.",
    intro:
      "Rapor koleksiyonunda ara, destekleyici pasajları incele ve bulguları yapılandırılmış bir politika notuna dönüştür.",
    questionLabel: "Soru",
    analyzing: "Kanıt analiz ediliyor",
    run: "Analizi başlat",
    documents: "belge",
    sources: "kaynak",
    status: "durum",
    ready: "Hazır",
    busy: "Çalışıyor",
    addReport: "Rapor ekle",
    providerLabel: "AI sağlayıcı",
    providerHelp: "Otomatik seçenek ayarlı sağlayıcıları sırayla dener ve gerekirse güvenli yedeğe döner.",
    providers: {
      auto: "Otomatik",
      groq: "Groq",
      gemini: "Gemini",
      openrouter: "OpenRouter",
    },
    providerUsed: "sağlayıcı",
    signalEvidence: "Kanıt indeksi",
    signalEvidenceText: "aranabilir belge",
    signalRouting: "AI yönlendirme",
    signalRoutingText: "seçili sağlayıcı",
    signalWorkflow: "Ajan iş akışı",
    signalWorkflowText: "kontrollü adım",
    sampleIndexed: "Örnek raporlar zaten indekslenmiş durumda.",
    upload: "PDF/TXT yükle",
    uploading: "Yükleniyor",
    indexing: "İşleniyor",
    uploadFailed: "Yükleme başarısız. PDF veya TXT dosyasıyla tekrar dene.",
    indexedDocuments: "İndekslenen kütüphane",
    indexedHelp: "Public demoda yüklenen dosya adları ve pasajları maskelenir.",
    refresh: "Yenile",
    noDocuments: "Henüz indekslenmiş belge bulunamadı.",
    chunk: "parça",
    consoleTitle: "Canlı ajan rotası",
    consoleText: "RAG arama -> LLM muhakeme -> politika notu",
    privacyTitle: "Gizlilik modu",
    privacyText: "Public izleyiciler sadece maskelenmiş yükleme etiketlerini görür.",
    stageReady: "Hazır",
    stageSearching: "İndekslenen belgelerde aranıyor",
    stageRetrieving: "Kanıtlar getiriliyor",
    stageWriting: "Cevap ve brief yazılıyor",
    stageComplete: "Analiz tamamlandı",
    stageFallback: "Yedek cevap gösterildi",
    stageIndexing: "Yüklenen belge indeksleniyor",
    stageIndexed: "Belge indekslendi",
    stageUploadFailed: "Yükleme başarısız",
    stageHelp:
      "Yükleme, belgeleri kanıt indeksine ekler. Analiz çalışınca sistem bu belgelerde arama yapar ve en güçlü kaynak pasajlarını döndürür.",
    result: "Analiz sonucu",
    sourceAware: "Kaynaklı",
    tabs: {
      answer: "Cevap",
      brief: "Politika notu",
      sources: "Kaynaklar",
      validation: "Doğrulama",
    },
    workflow: [
      { step: "Getir", description: "İlgili rapor bölümlerini bul", key: "research" },
      { step: "Analiz et", description: "En güçlü kanıtı özetle", key: "analysis" },
      { step: "Doğrula", description: "Kaynak kapsamını kontrol et", key: "validation" },
      { step: "Brief yaz", description: "Politika önerisini hazırla", key: "brief" },
    ],
    exampleQuestion: "Özel sektör finansmanı SKA uygulamasını nasıl destekleyebilir?",
    uploadedQuestion: () => "Yüklenen belgedeki ana bulgular ve öneriler nelerdir?",
    indexedMessage: (_fileName: string, chunks: number) => `Yüklenen belge ${chunks} parça olarak indekslendi.`,
    uploadingMessage: (fileName: string) => `${fileName} yükleniyor`,
  },
};

const exampleResponses: Record<Language, ResearchResponse> = {
  en: {
    question: copy.en.exampleQuestion,
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
    provider_used: "local",
  },
  tr: {
    question: copy.tr.exampleQuestion,
    answer:
      "Özel sektör finansmanı, yatırım kapasitesini artırarak, yeniliklerin yayılmasını hızlandırarak ve kamu bütçelerinin sınırlı kaldığı alanlarda finansman açığını azaltarak SKA uygulamasını destekleyebilir.",
    policy_brief:
      "Problem: SKA uygulaması çoğu zaman finansman kısıtlarıyla karşılaşır.\n\nKanıt: Kalkınma finansmanı literatürü karma finansman, risk paylaşımı ve özel sermaye mobilizasyonunun önemini vurgular.\n\nÖneri: Şeffaf finansman mekanizmaları kurulmalı, ölçülebilir etki hedefleri tanımlanmalı ve özel sektör katılımının kapsayıcılığı artırıp artırmadığı izlenmelidir.",
    sources: [
      {
        title: "Örnek kalkınma politikası raporu",
        location: "Sayfa 12",
        excerpt: "Risk paylaşımı mekanizmaları şeffaf olduğunda karma finansman özel sermayeyi harekete geçirebilir.",
      },
      {
        title: "Örnek SKA finansmanı notu",
        location: "Sayfa 4",
        excerpt: "Etki ölçümü, özel yatırımın kalkınma sonuçlarıyla uyumlu olması için gereklidir.",
      },
    ],
    validation_notes: ["2 destekleyici kaynak bulundu", "Politika notu problem, kanıt ve öneri bölümlerini içeriyor"],
    workflow_steps: ["research", "analysis", "validation", "brief"],
    provider_used: "local",
  },
};

const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL || `${window.location.protocol}//${window.location.hostname}:8000`;

const workflowIcons: Record<string, LucideIcon> = {
  research: FileSearch,
  analysis: LineChart,
  validation: ShieldCheck,
  brief: BookOpenText,
};

function getClientId() {
  const storageKey = "sdg-policy-client-id";
  const existing = window.localStorage.getItem(storageKey);
  if (existing) {
    return existing;
  }

  const generated =
    window.crypto?.randomUUID?.() || `client-${Date.now()}-${Math.random().toString(16).slice(2)}`;
  window.localStorage.setItem(storageKey, generated);
  return generated;
}

function App() {
  const [language, setLanguage] = useState<Language>("en");
  const t = copy[language];
  const [question, setQuestion] = useState(exampleResponses.en.question);
  const [result, setResult] = useState<ResearchResponse>(exampleResponses.en);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState(copy.en.sampleIndexed);
  const [documents, setDocuments] = useState<IndexedDocument[]>([]);
  const [provider, setProvider] = useState<Provider>("auto");
  const [currentStage, setCurrentStage] = useState(copy.en.stageReady);
  const [activeTab, setActiveTab] = useState<TabId>("answer");
  const [clientId] = useState(getClientId);

  function switchLanguage(nextLanguage: Language) {
    setLanguage(nextLanguage);
    setQuestion(exampleResponses[nextLanguage].question);
    setResult(exampleResponses[nextLanguage]);
    setUploadMessage(copy[nextLanguage].sampleIndexed);
    setCurrentStage(copy[nextLanguage].stageReady);
  }

  async function refreshDocuments() {
    try {
      const response = await fetch(`${apiBaseUrl}/documents`, {
        headers: { "X-Client-Id": clientId },
      });
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
  }, [clientId]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setCurrentStage(String(t.stageSearching));

    try {
      await new Promise((resolve) => window.setTimeout(resolve, 250));
      setCurrentStage(String(t.stageRetrieving));
      const response = await fetch(`${apiBaseUrl}/research`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, language, provider, client_id: clientId }),
      });

      if (!response.ok) {
        throw new Error("Request failed");
      }

      setCurrentStage(String(t.stageWriting));
      setResult(await response.json());
      setCurrentStage(String(t.stageComplete));
    } catch {
      setResult({ ...exampleResponses[language], question });
      setCurrentStage(String(t.stageFallback));
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
    setUploadMessage(t.uploadingMessage(file.name));
    setCurrentStage(String(t.stageIndexing));

    try {
      const response = await fetch(`${apiBaseUrl}/documents/upload`, {
        method: "POST",
        headers: { "X-Client-Id": clientId },
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      const payload = await response.json();
      setUploadMessage(t.indexedMessage(payload.file_name, payload.chunks));
      await refreshDocuments();
      setQuestion(t.uploadedQuestion(payload.file_name));
      setCurrentStage(String(t.stageIndexed));
    } catch {
      setUploadMessage(String(t.uploadFailed));
      setCurrentStage(String(t.stageUploadFailed));
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
            <small>{String(t.workspace)}</small>
          </div>
        </div>
        <div className="topbarActions">
          <nav className="navPills" aria-label="Workspace status">
            {(t.pills as string[]).map((pill) => (
              <span key={pill}>{pill}</span>
            ))}
          </nav>
          <div className="languageToggle" aria-label="Language selector">
            <button type="button" className={language === "en" ? "active" : ""} onClick={() => switchLanguage("en")}>
              EN
            </button>
            <button type="button" className={language === "tr" ? "active" : ""} onClick={() => switchLanguage("tr")}>
              TR
            </button>
          </div>
        </div>
      </header>

      <section className="agentConsole" aria-label="Agent console">
        <div>
          <span>{String(t.consoleTitle)}</span>
          <strong>{String(t.consoleText)}</strong>
        </div>
        <div className="consoleSignals" aria-hidden="true">
          <i />
          <i />
          <i />
        </div>
        <div>
          <span>{String(t.privacyTitle)}</span>
          <strong>{String(t.privacyText)}</strong>
        </div>
      </section>

      <section className="workspace">
        <aside className="queryPanel">
          <div className="panelTitle">
            <Network size={18} />
            {String(t.panelTitle)}
          </div>
          <h1>{String(t.headline)}</h1>
          <p>{String(t.intro)}</p>

          <form className="questionBox" onSubmit={handleSubmit}>
            <label htmlFor="research-question">{String(t.questionLabel)}</label>
            <textarea
              id="research-question"
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              aria-label={String(t.questionLabel)}
            />
            <button type="submit" disabled={loading}>
              {loading ? String(t.analyzing) : String(t.run)}
              <ArrowRight size={18} />
            </button>
          </form>

          <div className="providerPanel">
            <div>
              <strong>{String(t.providerLabel)}</strong>
              <span>{String(t.providerHelp)}</span>
            </div>
            <select value={provider} onChange={(event) => setProvider(event.target.value as Provider)}>
              {(["auto", "groq", "gemini", "openrouter"] as Provider[]).map((option) => (
                <option key={option} value={option}>
                  {t.providers[option]}
                </option>
              ))}
            </select>
          </div>

          <div className="metricStrip">
            <div>
              <strong>{documents.length}</strong>
              <span>{String(t.documents)}</span>
            </div>
            <div>
              <strong>{result.sources.length}</strong>
              <span>{String(t.sources)}</span>
            </div>
            <div>
              <strong>{result.provider_used}</strong>
              <span>{String(t.providerUsed)}</span>
            </div>
          </div>

          <div className="uploadPanel">
            <div>
              <strong>{String(t.addReport)}</strong>
              <span>{uploadMessage}</span>
            </div>
            <label className={uploading ? "uploadButton disabled" : "uploadButton"}>
              {uploading ? String(t.indexing) : String(t.upload)}
              <input type="file" accept=".pdf,.txt" onChange={handleUpload} disabled={uploading} />
            </label>
          </div>

          <div className="documentsPanel">
            <div className="documentsHeader">
              <div>
                <strong>{String(t.indexedDocuments)}</strong>
                <span>{String(t.indexedHelp)}</span>
              </div>
              <button type="button" onClick={refreshDocuments}>{String(t.refresh)}</button>
            </div>
            {documents.length === 0 ? (
              <p>{String(t.noDocuments)}</p>
            ) : (
              <div className="documentList">
                {documents.map((document) => (
                  <button
                    type="button"
                    className="documentItem"
                    key={document.file_name}
                    onClick={() => setQuestion(t.uploadedQuestion(document.file_name))}
                  >
                    <span>{document.title}</span>
                    <small>{document.file_name} · {document.chunks} {String(t.chunk)} · {document.source_type}</small>
                  </button>
                ))}
              </div>
            )}
          </div>
        </aside>

        <section className="analysisPanel">
          <div className="workflowRail" aria-label="Workflow">
            {(t.workflow as Array<{ step: string; description: string; key: string }>).map(({ step, description, key }, index) => {
              const Icon = workflowIcons[key];
              return (
                <div className={result.workflow_steps?.includes(key) ? "workflowStep complete" : "workflowStep"} key={key}>
                  <span>{index + 1}</span>
                  <div>
                    <strong>{step}</strong>
                    <p>{description}</p>
                  </div>
                  <Icon size={18} />
                </div>
              );
            })}
          </div>

          <div className="stageBanner">
            <span>{currentStage}</span>
            <p>{String(t.stageHelp)}</p>
            {(loading || uploading) && <div className="activityLine" aria-hidden="true" />}
          </div>

          <div className="signalGrid" aria-label="System summary">
            <div className="signalCard">
              <span>{String(t.signalEvidence)}</span>
              <strong>{documents.length}</strong>
              <small>{String(t.signalEvidenceText)}</small>
            </div>
            <div className="signalCard">
              <span>{String(t.signalRouting)}</span>
              <strong>{provider}</strong>
              <small>{String(t.signalRoutingText)}</small>
            </div>
            <div className="signalCard">
              <span>{String(t.signalWorkflow)}</span>
              <strong>{result.workflow_steps?.length || 0}</strong>
              <small>{String(t.signalWorkflowText)}</small>
            </div>
          </div>

          <article className="resultPanel">
            <div className="resultHeader">
              <div>
                <div className="sectionLabel">
                  <Layers3 size={18} />
                  {String(t.result)}
                </div>
                <h2>{result.question}</h2>
              </div>
              <div className="qualityBadge">
                <Sparkles size={16} />
                {String(t.sourceAware)}
              </div>
            </div>

            <div className="tabs" role="tablist" aria-label="Analysis sections">
              {(["answer", "brief", "sources", "validation"] as TabId[]).map((id) => (
                <button
                  key={id}
                  type="button"
                  className={activeTab === id ? "active" : ""}
                  onClick={() => setActiveTab(id)}
                >
                  {t.tabs[id]}
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
