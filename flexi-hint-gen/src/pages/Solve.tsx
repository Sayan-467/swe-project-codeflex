import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Code2, Lightbulb, Send, ChevronRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import "highlight.js/styles/github.css"; // Optional styling

const Solve = () => {
  interface Hint {
  hint: string;
  }

  const navigate = useNavigate();
  const [link, setLink] = useState("");
  const [hints, setHints] = useState<Hint[]>([]);
  const [currentHintIndex, setCurrentHintIndex] = useState(-1);
  const [chatMessages, setChatMessages] = useState<Array<{ role: "user" | "assistant"; content: string }>>([]);
  const [chatInput, setChatInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isCodeChef,setisCodeChef] = useState(false);
  const [url, setUrl] = useState("");
  const [notFound,setnotfound] = useState("");
  const [thinking,setthinking] = useState(false);
  
  function extractJsonArray(text: string) {
  try {
    // Try to match a fenced JSON code block: ```json ... ```
    const codeBlockMatch = text.match(/```(?:json)?\s*(\[[\s\S]*?\])\s*```/);
    let jsonStr: string | null = null;

    if (codeBlockMatch) {
      jsonStr = codeBlockMatch[1];
    } else {
      // Fallback: look for any JSON array in the string
      const arrayMatch = text.match(/(\[[\s\S]*?\])/);
      if (arrayMatch) {
        jsonStr = arrayMatch[1];
      }
    }

    if (!jsonStr) return null;

    return JSON.parse(jsonStr.trim());
  } catch (err) {
    console.error("JSON parse error:", err);
    return null;
  }
}

  const checkCodechef = (url : string) => {
    if(url.split("://")[1].split(".")[1].toLowerCase() === "codechef"){
    setisCodeChef(true);
    return true;
  }
    setisCodeChef(false)
    return false
  }

  const handleFetchSolution = async() => {
    if (!link.trim()) return;

    setIsLoading(true);
    const isCodeChef = checkCodechef(link);
    try{
      if (isCodeChef) {
        console.log(isCodeChef);
        const res = await fetch(
        `http://localhost:8001/codechef/generate/hints`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ problem_url: link })
      });
      console.log(res);
      if (res.ok) {
        console.log("Fetch success!");
        const data = await res.json(); // ✅ await and expect JSON
        const hints = extractJsonArray(data.generated_hints)
        console.log(hints);
        setHints(hints);
        console.log(data);
      } else {
        const text = await res.text(); // fallback to see the raw error
        console.error("Error response:", text);
        setnotfound(text);
      }
    }
    else{
      const res = await fetch(
        `http://localhost:8001/codeforces/generate/hints`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ problem_url: link })
      });
      console.log(res);
      if (res.ok) {
        console.log("Fetch success!");
        const data = await res.json(); // ✅ await and expect JSON
        setHints(data.generated_hints);
        console.log(data);
      } else {
        const text = await res.text(); // fallback to see the raw error
        console.error("Error response:", text);
      }
    }
  }
    catch(e){
      console.log(e);
    }
    setIsLoading(false);
  };

  const handleShowNextHint = () => {
    if (currentHintIndex < hints.length - 1) {
      setCurrentHintIndex(currentHintIndex + 1);
    }
  };

  const handleSendMessage = async() => {
    if (!chatInput.trim()) return;
    const newMessage = { role: "user" as const, content: chatInput };
    setChatMessages(prev => [...prev, newMessage]);

    setChatInput("");
    try{
      setthinking(true);
      const res = await fetch(
        `http://localhost:8002/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          message: chatInput, 
          context : []
        })
      });

      if(res.ok){
        const data = await res.json()
        console.log(data.reply);
        const newMessage = { role: "assistant" as const, content: data.reply || data.message || "No response" };
        setChatMessages(prev => [...prev, newMessage]);
        setthinking(false);
      }
    }
    catch(e){
      console.log(e);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <button onClick={() => navigate("/")} className="flex items-center space-x-2 hover:opacity-80 transition-opacity">
              <Code2 className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold">Codeflex</span>
            </button>
            <Button variant="ghost" onClick={() => navigate("/")}>
              Home
            </Button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Input Form */}
        <Card className="p-6 mb-8 border-border bg-card">
          <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
            <Lightbulb className="h-6 w-6 text-primary" />
            Get Hints for Your Problem
          </h2>
          <div className="flex p-4 gap-3">
            <Input
              placeholder="Paste your LeetCode, HackerRank, or CodeChef link here..."
              value={link}
              onChange={(e) => setLink(e.target.value)}
              className="flex-1 p-2"
            />
            <Button onClick={handleFetchSolution} disabled={isLoading || !link.trim()} className="px-8">
              {isLoading ? "Loading..." : "Get Hints"}
            </Button>
          </div>
        </Card>

        {notFound != "" ? 
        <div className="bg-red-400 flex items-center justify-center">
            `${notFound}`
        </div> : <></>}
        
        {/* Results Section - Only show when hints are available */}
        {hints?.length > 0 && (  
          <div className="grid lg:grid-cols-2 gap-6">
            {/* Hints Panel */}
            <Card className="p-6 border-border bg-card">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-bold">Generated Hints</h3>
                <span className="text-sm text-muted-foreground">
                  {currentHintIndex + 1} / {hints.length}
                </span>
              </div>

              <div className="space-y-4 mb-6">
                {hints.slice(0, currentHintIndex + 1).map((hintObj, index) => (
                <div
                  key={index}
                  className="p-4 rounded-lg bg-secondary/50 border border-border animate-in slide-in-from-bottom-2 duration-300"
                >
                  <div className="flex gap-3">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                      {index + 1}
                    </div>
                    <p className="text-foreground flex-1 pt-1">{hintObj.hint}</p>
                  </div>
                </div>
              ))}
              </div>

              {currentHintIndex < hints.length - 1 && (
                <Button onClick={handleShowNextHint} className="w-full group" size="lg">
                  Show Next Hint
                  <ChevronRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              )}

              {currentHintIndex === hints.length - 1 && (
                <div className="text-center p-4 rounded-lg bg-primary/10 border border-primary/30">
                  <p className="text-primary font-medium">All hints revealed! Try solving it now.</p>
                </div>
              )}
            </Card>

            {/* Chatbot Panel */}
            <Card className="p-6 border-border bg-card flex flex-col h-[600px]">
              <h3 className="text-xl font-bold mb-4">AI Assistant</h3>

              <div className="flex-1 overflow-y-auto space-y-4 mb-4 pr-2">
                {chatMessages.length === 0 ? (
                  <div className="text-center text-muted-foreground py-12">
                    <p>Ask me anything about the problem!</p>
                  </div>
                ) : (
                  <>
                    {chatMessages.map((message, index) => (
                      <div
                        key={index}
                        className={`p-3 rounded-lg ${
                          message.role === "user"
                            ? "bg-primary/20 ml-8"
                            : "bg-secondary/50 mr-8"
                        } animate-in slide-in-from-bottom-2 duration-300`}
                      >
                      <p className="text-sm font-white">
                      {message.content}
                    </p>
                      </div>
                    ))}

                    {/* Loader when thinking */}
                    {thinking && (
                      <div className="p-3 rounded-lg bg-secondary/50 mr-8 flex items-center gap-2">
                        <div className="w-4 h-4 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
                        <p className="text-sm text-muted-foreground">Thinking...</p>
                      </div>
                    )}
                  </>
                )}
              </div>

              <div className="flex gap-2 border-t border-border pt-4">
                <Textarea
                  placeholder="Ask about the problem, hints, or concepts..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault();
                      handleSendMessage();
                    }
                  }}
                  className="resize-none min-h-[60px]"
                />
                <Button
                  onClick={handleSendMessage}
                  disabled={!chatInput.trim() || thinking}
                  size="icon"
                  className="h-[60px] w-[60px]"
                >
                  <Send className="h-5 w-5" />
                </Button>
              </div>
            </Card>

          </div>
        )}
      </main>
    </div>
  );
};

export default Solve;
