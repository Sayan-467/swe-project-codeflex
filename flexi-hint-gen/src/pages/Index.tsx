import { useState } from "react";
import { Button } from "@/components/ui/button";
import { AuthModals } from "@/components/AuthModals";
import { useNavigate } from "react-router-dom";
import heroImage from "@/assets/hero-coding.jpg";
import { Code2, Zap, Target, ArrowRight } from "lucide-react";

const Index = () => {
  const [isSignInOpen, setIsSignInOpen] = useState(false);
  const [isSignUpOpen, setIsSignUpOpen] = useState(false);
  const navigate = useNavigate();

  const handleSwitchToSignUp = () => {
    setIsSignInOpen(false);
    setIsSignUpOpen(true);
  };

  const handleSwitchToSignIn = () => {
    setIsSignUpOpen(false);
    setIsSignInOpen(true);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 border-b border-border bg-background/80 backdrop-blur-lg">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-2">
              <Code2 className="h-8 w-8 text-primary" />
              <span className="text-xl font-bold">Codeflex</span>
            </div>
            <div className="flex items-center space-x-3">
              <Button variant="ghost" onClick={() => setIsSignInOpen(true)}>
                Sign In
              </Button>
              <Button onClick={() => setIsSignUpOpen(true)}>
                Sign Up
              </Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 opacity-20">
          <img src={heroImage} alt="Coding visualization" className="w-full h-full object-cover" />
        </div>
        <div className="relative container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 bg-gradient-to-r from-primary via-cyan-400 to-primary bg-clip-text text-transparent animate-in fade-in slide-in-from-bottom-4 duration-1000">
              Master Problem Solving
            </h1>
            <p className="text-xl sm:text-2xl text-muted-foreground mb-8 animate-in fade-in slide-in-from-bottom-5 duration-1000 delay-150">
              Transform any coding challenge into step-by-step hints. Learn smarter, not harder.
            </p>
            <Button 
              size="lg" 
              className="group px-8 shadow-[0_0_40px_hsl(var(--primary)/0.3)] hover:shadow-[0_0_60px_hsl(var(--primary)/0.5)] transition-all animate-in fade-in slide-in-from-bottom-6 duration-1000 delay-300"
              onClick={() => navigate("/solve")}
            >
              Start Solving
              <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-card/50">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 rounded-lg bg-card border border-border hover:border-primary/50 transition-all hover:shadow-[0_0_30px_hsl(var(--primary)/0.2)]">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold mb-2">Instant Hints</h3>
              <p className="text-muted-foreground">
                Get AI-powered hints instantly from any coding platform link. No more getting stuck.
              </p>
            </div>
            <div className="p-6 rounded-lg bg-card border border-border hover:border-primary/50 transition-all hover:shadow-[0_0_30px_hsl(var(--primary)/0.2)]">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Target className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold mb-2">Structured Learning</h3>
              <p className="text-muted-foreground">
                Reveal hints one by one to guide your thinking process without spoiling the solution.
              </p>
            </div>
            <div className="p-6 rounded-lg bg-card border border-border hover:border-primary/50 transition-all hover:shadow-[0_0_30px_hsl(var(--primary)/0.2)]">
              <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <Code2 className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold mb-2">AI Assistant</h3>
              <p className="text-muted-foreground">
                Chat with an AI tutor to deepen your understanding and clarify concepts.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto text-center bg-gradient-to-r from-card to-card/50 p-12 rounded-2xl border border-border">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4">
              Ready to Level Up Your Problem Solving?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Join developers who are mastering algorithms with AI-powered guidance.
            </p>
            <Button size="lg" onClick={() => setIsSignUpOpen(true)} className="px-8">
              Get Started Free
            </Button>
          </div>
        </div>
      </section>

      <AuthModals
        isSignInOpen={isSignInOpen}
        isSignUpOpen={isSignUpOpen}
        onSignInClose={() => setIsSignInOpen(false)}
        onSignUpClose={() => setIsSignUpOpen(false)}
        onSwitchToSignUp={handleSwitchToSignUp}
        onSwitchToSignIn={handleSwitchToSignIn}
      />
    </div>
  );
};

export default Index;
