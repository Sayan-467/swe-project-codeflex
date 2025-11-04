import { useState } from "react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

interface AuthModalsProps {
  isSignInOpen: boolean;
  isSignUpOpen: boolean;
  onSignInClose: () => void;
  onSignUpClose: () => void;
  onSwitchToSignUp: () => void;
  onSwitchToSignIn: () => void;
}

export const AuthModals = ({
  isSignInOpen,
  isSignUpOpen,
  onSignInClose,
  onSignUpClose,
  onSwitchToSignUp,
  onSwitchToSignIn,
}: AuthModalsProps) => {
  const [rememberMe, setRememberMe] = useState(false);

  return (
    <>
      {/* Sign In Modal */}
      <Dialog open={isSignInOpen} onOpenChange={onSignInClose}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-2xl font-bold">Welcome Back</DialogTitle>
            <DialogDescription>Sign in to continue your coding journey</DialogDescription>
          </DialogHeader>
          <form className="space-y-4 mt-4">
            <div className="space-y-2">
              <Label htmlFor="signin-email">Email</Label>
              <Input id="signin-email" type="email" placeholder="you@example.com" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="signin-password">Password</Label>
              <Input id="signin-password" type="password" placeholder="••••••••" />
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Checkbox id="remember" checked={rememberMe} onCheckedChange={(checked) => setRememberMe(checked as boolean)} />
                <Label htmlFor="remember" className="text-sm cursor-pointer">Remember me</Label>
              </div>
              <button type="button" className="text-sm text-primary hover:underline">
                Forgot password?
              </button>
            </div>
            <Button type="submit" className="w-full" size="lg">
              Sign In
            </Button>
            <p className="text-center text-sm text-muted-foreground">
              Don't have an account?{" "}
              <button type="button" onClick={onSwitchToSignUp} className="text-primary hover:underline">
                Sign up
              </button>
            </p>
          </form>
        </DialogContent>
      </Dialog>

      {/* Sign Up Modal */}
      <Dialog open={isSignUpOpen} onOpenChange={onSignUpClose}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="text-2xl font-bold">Create Account</DialogTitle>
            <DialogDescription>Start your problem-solving journey today</DialogDescription>
          </DialogHeader>
          <form className="space-y-4 mt-4">
            <div className="space-y-2">
              <Label htmlFor="signup-name">Full Name</Label>
              <Input id="signup-name" type="text" placeholder="John Doe" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="signup-email">Email</Label>
              <Input id="signup-email" type="email" placeholder="you@example.com" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="signup-password">Password</Label>
              <Input id="signup-password" type="password" placeholder="••••••••" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="signup-confirm">Confirm Password</Label>
              <Input id="signup-confirm" type="password" placeholder="••••••••" />
            </div>
            <Button type="submit" className="w-full" size="lg">
              Create Account
            </Button>
            <p className="text-center text-sm text-muted-foreground">
              Already have an account?{" "}
              <button type="button" onClick={onSwitchToSignIn} className="text-primary hover:underline">
                Sign in
              </button>
            </p>
          </form>
        </DialogContent>
      </Dialog>
    </>
  );
};
