'use client';

import { FormEvent, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  ArrowRight,
  ArrowUp,
  BookOpen,
  BriefcaseBusiness,
  CheckCircle2,
  Code2,
  ExternalLink,
  FileText,
  LoaderCircle,
  Mail,
  MapPin,
  MessageCircleMore,
  Network,
  RotateCcw,
  Sparkles,
} from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';

const PORTFOLIO_URL =
  'https://app.notion.com/p/Portfolio-Marc-Navarro-386a73a4ed5280efa99bd47efb571508';
const API_URL = (
  import.meta.env.VITE_API_URL ||
  'https://marc-gpt-api-352673032677.europe-west1.run.app'
).replace(/\/$/, '');

const suggestions = [
  'What makes Marc a strong data professional?',
  'Tell me about his renewable energy experience',
  'Tell me about Marc’s PV Dome project',
  'How has Marc led international teams?',
];

const projects = [
  {
    name: 'PV Dome',
    detail: 'Next.js · Supabase · Python',
    description:
      'A full-stack MVP for modelling solar PV portfolios, projections, operations and financial performance.',
    github: 'https://github.com/navaso93/pv_assets',
    color: 'from-violet-100 to-fuchsia-50',
  },
  {
    name: 'LIAR classifier',
    detail: 'NLP · XGBoost · RAG',
    description:
      'A political-statement classification pipeline combining LIAR and Politifact data with grounded Gemini explanations.',
    github: 'https://github.com/navaso93/liar_project',
    color: 'from-amber-100 to-orange-50',
  },
  {
    name: 'Marc GPT',
    detail: 'FastAPI · Gemini · ChromaDB',
    description:
      'A conversational CV grounded in a public Markdown knowledge base, built for recruiter-style exploration.',
    github: 'https://github.com/navaso93/me-gpt',
    color: 'from-sky-100 to-cyan-50',
  },
  {
    name: 'Seeding Impact',
    detail: 'Climate · Entrepreneurship',
    description:
      'A student-led platform connecting sustainability education with incubators in developing countries.',
    github: '',
    color: 'from-emerald-100 to-lime-50',
  },
];

function MarkdownResponse({ content }: { content: string }) {
  return (
    <div className="markdown-response text-sm text-foreground/80">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          a: ({ node: _node, ...props }) => (
            <a {...props} target="_blank" rel="noreferrer" />
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

export default function Home() {
  const [question, setQuestion] = useState('');
  const [submitted, setSubmitted] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [fitAnswer, setFitAnswer] = useState('');
  const [fitLoading, setFitLoading] = useState(false);
  const [fitError, setFitError] = useState('');

  async function submit(event?: FormEvent) {
    event?.preventDefault();
    if (!question.trim()) return;
    const outgoing = question.trim();
    setSubmitted(outgoing);
    setQuestion('');
    setAnswer('');
    setError('');
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: outgoing }),
      });
      if (!response.ok) throw new Error();
      const data = (await response.json()) as { answer: string };
      setAnswer(data.answer);
    } catch {
      setError(
        'The knowledge service is not connected to this deployment yet.',
      );
    } finally {
      setLoading(false);
    }
  }

  async function evaluateFit(event: FormEvent) {
    event.preventDefault();
    if (!jobDescription.trim()) return;
    setFitAnswer('');
    setFitError('');
    setFitLoading(true);
    try {
      const response = await fetch(`${API_URL}/job_fit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ job_description: jobDescription.trim() }),
      });
      if (!response.ok) throw new Error();
      const data = (await response.json()) as { answer: string };
      setFitAnswer(data.answer);
    } catch {
      setFitError(
        'The knowledge service is not connected to this deployment yet.',
      );
    } finally {
      setFitLoading(false);
    }
  }

  function askAbout(project: string) {
    setQuestion(`Tell me about Marc's ${project} project`);
    setSubmitted('');
    setAnswer('');
    document.querySelector('#profile')?.scrollIntoView({ behavior: 'smooth' });
  }

  return (
    <main className="h-screen overflow-hidden bg-background text-foreground lg:grid lg:grid-cols-[300px_minmax(0,1fr)]">
      <aside className="border-b border-border bg-sidebar px-5 py-5 lg:h-screen lg:overflow-y-auto lg:border-b-0 lg:border-r lg:px-7 lg:py-8">
        <div className="flex items-center gap-4 lg:block">
          <Avatar className="size-16 ring-4 ring-white shadow-sm lg:size-24">
            <AvatarImage src="/profile.jpg" alt="Marc Navarro Sotés" />
            <AvatarFallback>MN</AvatarFallback>
          </Avatar>
          <div className="lg:mt-5">
            <h1 className="text-xl font-semibold tracking-tight">
              Marc Navarro Sotés
            </h1>
            <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
              Data & AI professional with deep renewable-energy experience.
            </p>
          </div>
        </div>
        <div className="mt-4 flex items-center gap-2 text-sm text-muted-foreground">
          <MapPin className="size-4 text-primary" /> Berlin, Germany
        </div>

        <div className="mt-6">
          <p className="sidebar-heading">Explore & connect</p>
          <div className="mt-3 grid grid-cols-2 gap-2">
            <Button
              className="col-span-2 h-10"
              nativeButton={false}
              render={
                <a href={PORTFOLIO_URL} target="_blank" rel="noreferrer" />
              }
            >
              <BookOpen /> Portfolio <ExternalLink className="ml-auto" />
            </Button>
            <Button
              variant="outline"
              nativeButton={false}
              render={
                <a
                  href="https://github.com/navaso93"
                  target="_blank"
                  rel="noreferrer"
                />
              }
            >
              <Code2 /> GitHub
            </Button>
            <Button
              variant="outline"
              nativeButton={false}
              render={
                <a
                  href="https://linkedin.com/in/marc-navarro-sotés/"
                  target="_blank"
                  rel="noreferrer"
                />
              }
            >
              <Network /> LinkedIn
            </Button>
            <Button
              variant="outline"
              nativeButton={false}
              render={
                <a
                  href="/marc-navarro-cv.pdf"
                  target="_blank"
                  rel="noreferrer"
                />
              }
            >
              <FileText /> CV
            </Button>
            <Button
              variant="outline"
              nativeButton={false}
              render={<a href="mailto:mnavarrosotes@gmail.com" />}
            >
              <Mail /> Email
            </Button>
          </div>
        </div>

        <div className="mt-7">
          <p className="sidebar-heading">Experienced with</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {[
              'Python',
              'SQL',
              'BigQuery',
              'dbt',
              'RAG',
              'FastAPI',
              'Solar PV',
            ].map((skill) => (
              <Badge
                key={skill}
                variant="secondary"
                className="h-6 bg-white px-2.5 text-[11px]"
              >
                {skill}
              </Badge>
            ))}
          </div>
        </div>

        <nav
          className="mt-8 hidden space-y-1 border-t border-border pt-6 lg:block"
          aria-label="Page sections"
        >
          <a className="nav-link nav-link-active" href="#profile">
            <MessageCircleMore /> AI profile
          </a>
          <a className="nav-link" href="#role-fit">
            <BriefcaseBusiness /> Role compatibility
          </a>
          <a className="nav-link" href="#selected-work">
            <Sparkles /> Selected work
          </a>
        </nav>
        <p className="mt-8 hidden text-[11px] leading-5 text-muted-foreground lg:block">
          Marc GPT answers from a public, curated knowledge base and should say
          when information is unavailable.
        </p>
      </aside>

      <div className="content-canvas h-[calc(100vh-121px)] overflow-y-auto scroll-smooth lg:h-screen">
        <div className="content-column">
          <section id="profile" className="section-shell">
            <div className="section-kicker">
              <span className="status-dot" /> AI profile · online
            </div>
            <h2 className="mt-3 text-3xl font-semibold tracking-[-.035em] sm:text-4xl">
              Ask me anything about Marc.
            </h2>
            <p className="mt-2 max-w-2xl text-muted-foreground">
              Explore his experience, projects, technical skills and leadership
              through a grounded conversation.
            </p>

            <div className="mt-8 max-w-4xl rounded-3xl border border-border bg-white p-5 shadow-[0_12px_40px_rgb(24_32_29/7%)] sm:p-7">
              <form onSubmit={submit}>
                <div className="chat-composer">
                  <Textarea
                    value={question}
                    onChange={(event) => setQuestion(event.target.value)}
                    onKeyDown={(event) => {
                      if (event.key === 'Enter' && !event.shiftKey) {
                        event.preventDefault();
                        submit();
                      }
                    }}
                    aria-label="Ask Marc GPT a question"
                    placeholder="Ask about Marc’s experience, projects or skills…"
                    className="min-h-14 resize-none border-0 bg-transparent px-1 py-2 shadow-none focus-visible:ring-0"
                  />
                  <Button
                    type="submit"
                    size="icon"
                    className="size-10 rounded-xl"
                    disabled={!question.trim() || loading}
                    aria-label="Send question"
                  >
                    {loading ? (
                      <LoaderCircle className="animate-spin" />
                    ) : (
                      <ArrowUp />
                    )}
                  </Button>
                </div>
                <p className="mt-2 text-center text-[11px] text-muted-foreground">
                  Press Enter to send · Shift + Enter for a new line
                </p>
              </form>

              {submitted && (
                <div className="mt-7 border-t border-border pt-7">
                  <div className="ml-auto max-w-[85%] rounded-2xl rounded-br-md bg-foreground px-5 py-3.5 text-sm leading-6 text-background">
                    {submitted}
                  </div>
                  <div className="mt-6 flex gap-3">
                    <div className="assistant-mark shrink-0">
                      <Sparkles className="size-4" />
                    </div>
                    <div className="min-w-0 flex-1">
                      {loading ? (
                        <p className="flex items-center gap-2 py-2 text-sm text-muted-foreground">
                          <LoaderCircle className="size-4 animate-spin" />{' '}
                          Searching Marc&apos;s profile…
                        </p>
                      ) : error ? (
                        <p className="whitespace-pre-wrap text-sm leading-7 text-destructive">
                          {error}
                        </p>
                      ) : (
                        <MarkdownResponse content={answer} />
                      )}
                      <div className="mt-3 flex items-center justify-between gap-3">
                        <p className="text-xs font-medium text-muted-foreground">
                          Grounded in Marc&apos;s knowledge base
                        </p>
                        <Button
                          type="button"
                          variant="ghost"
                          size="xs"
                          onClick={() => {
                            setSubmitted('');
                            setAnswer('');
                            setError('');
                          }}
                        >
                          <RotateCcw /> Clear
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              <div className="mt-7 border-t border-border pt-6">
                <p className="text-xs font-semibold uppercase tracking-[.13em] text-muted-foreground">
                  Good places to start
                </p>
                <div className="mt-3 grid gap-2 sm:grid-cols-2">
                  {suggestions.map((item) => (
                    <button
                      key={item}
                      type="button"
                      className="suggestion-row"
                      onClick={() => setQuestion(item)}
                    >
                      <span>{item}</span>
                      <ArrowUp className="size-3.5 rotate-45 text-primary" />
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </section>

          <section
            id="role-fit"
            className="section-shell border-t border-border bg-[#f7f8f5]"
          >
            <div className="section-kicker">
              <BriefcaseBusiness className="size-4" /> Role compatibility
            </div>
            <div className="mt-4 grid max-w-6xl gap-8 lg:grid-cols-[.72fr_1.28fr] lg:gap-12">
              <div>
                <h2 className="text-3xl font-semibold tracking-[-.035em] sm:text-4xl">
                  Compare Marc with your role.
                </h2>
                <p className="mt-4 leading-7 text-muted-foreground">
                  Paste the job description for an evidence-based view of strong
                  matches, transferable experience, potential gaps and interview
                  talking points.
                </p>
                <div className="mt-6 space-y-3">
                  {[
                    'Based on demonstrated experience',
                    'Transparent about gaps',
                    'Designed to inform an interview',
                  ].map((item) => (
                    <p
                      key={item}
                      className="flex items-center gap-3 text-sm font-medium"
                    >
                      <CheckCircle2 className="size-4 text-primary" />
                      {item}
                    </p>
                  ))}
                </div>
              </div>
              <form
                onSubmit={evaluateFit}
                className="rounded-3xl border border-border bg-white p-5 shadow-[0_8px_30px_rgb(24_32_29/5%)] sm:p-7"
              >
                <label
                  htmlFor="job-description"
                  className="text-sm font-semibold"
                >
                  Job description
                </label>
                <Textarea
                  id="job-description"
                  value={jobDescription}
                  onChange={(event) => setJobDescription(event.target.value)}
                  placeholder="Paste the complete job description here…"
                  className="mt-3 min-h-56 resize-y bg-background p-4 leading-6"
                />
                <Button
                  type="submit"
                  size="lg"
                  className="mt-4 h-11 w-full rounded-xl"
                  disabled={fitLoading || !jobDescription.trim()}
                >
                  {fitLoading ? (
                    <>
                      <LoaderCircle className="animate-spin" /> Evaluating…
                    </>
                  ) : (
                    <>
                      Evaluate compatibility <ArrowRight />
                    </>
                  )}
                </Button>
                {(fitAnswer || fitError) && (
                  <div
                    className={`mt-5 rounded-2xl border p-5 ${fitError ? 'border-destructive/20 bg-destructive/5' : 'border-primary/15 bg-[#fbf6f1]'}`}
                  >
                    {fitError ? (
                      <p className="whitespace-pre-wrap text-sm leading-7 text-destructive">
                        {fitError}
                      </p>
                    ) : (
                      <MarkdownResponse content={fitAnswer} />
                    )}
                  </div>
                )}
              </form>
            </div>
          </section>

          <section
            id="selected-work"
            className="section-shell border-t border-border"
          >
            <div className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
              <div>
                <div className="section-kicker">
                  <Sparkles className="size-4" /> Selected work
                </div>
                <h2 className="mt-4 text-3xl font-semibold tracking-[-.035em] sm:text-4xl">
                  Projects, with the full story.
                </h2>
              </div>
              <Button
                variant="outline"
                nativeButton={false}
                render={
                  <a href={PORTFOLIO_URL} target="_blank" rel="noreferrer" />
                }
              >
                <BookOpen /> Explore full portfolio <ExternalLink />
              </Button>
            </div>
            <div className="mt-8 grid max-w-6xl gap-5 md:grid-cols-2 xl:grid-cols-4">
              {projects.map((project, index) => (
                <article
                  key={project.name}
                  className="overflow-hidden rounded-3xl border border-border bg-white"
                >
                  <div
                    className={`flex h-32 items-end bg-gradient-to-br p-5 ${project.color}`}
                  >
                    <span className="text-xs font-bold tracking-[.16em] text-foreground/45">
                      PROJECT 0{index + 1}
                    </span>
                  </div>
                  <div className="p-5">
                    <Badge variant="secondary">{project.detail}</Badge>
                    <h3 className="mt-4 text-lg font-semibold">
                      {project.name}
                    </h3>
                    <p className="mt-2 min-h-24 text-sm leading-6 text-muted-foreground">
                      {project.description}
                    </p>
                    <div className="mt-4 flex flex-wrap gap-3">
                      <a
                        href={PORTFOLIO_URL}
                        target="_blank"
                        rel="noreferrer"
                        className="inline-flex items-center gap-1 text-sm font-semibold text-primary hover:underline"
                      >
                        Full story <ExternalLink className="size-3.5" />
                      </a>
                      {project.github && (
                        <a
                          href={project.github}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 text-sm font-medium text-muted-foreground hover:text-foreground"
                        >
                          <Code2 className="size-3.5" /> GitHub
                        </a>
                      )}
                      <button
                        type="button"
                        className="text-sm font-medium text-muted-foreground hover:text-primary"
                        onClick={() => askAbout(project.name)}
                      >
                        Ask Marc
                      </button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          </section>

          <footer className="border-t border-border bg-foreground px-5 py-10 text-background sm:px-10 lg:px-14">
            <div className="mx-auto flex max-w-6xl flex-col justify-between gap-5 sm:flex-row sm:items-center">
              <div>
                <p className="text-xs uppercase tracking-[.15em] text-background/55">
                  Marc Navarro Sotés
                </p>
                <p className="mt-2 text-xl font-semibold">
                  Data, AI and renewable energy.
                </p>
              </div>
              <Button
                className="bg-background text-foreground hover:bg-background/90"
                nativeButton={false}
                render={<a href="mailto:mnavarrosotes@gmail.com" />}
              >
                <Mail /> Get in touch
              </Button>
            </div>
          </footer>
        </div>
      </div>

      <nav
        className="fixed inset-x-4 bottom-4 z-50 flex items-center justify-around rounded-2xl border border-border bg-white/95 p-2 shadow-[0_12px_40px_rgb(24_32_29/16%)] backdrop-blur lg:hidden"
        aria-label="Mobile navigation"
      >
        <a className="mobile-nav-link" href="#profile">
          <MessageCircleMore /> Ask
        </a>
        <a className="mobile-nav-link" href="#role-fit">
          <BriefcaseBusiness /> Fit
        </a>
        <a className="mobile-nav-link" href="#selected-work">
          <Sparkles /> Work
        </a>
        <a
          className="mobile-nav-link"
          href={PORTFOLIO_URL}
          target="_blank"
          rel="noreferrer"
        >
          <BookOpen /> Portfolio
        </a>
      </nav>
    </main>
  );
}
