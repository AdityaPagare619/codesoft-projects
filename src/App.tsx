import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import MobileSignup from "./pages/MobileSignup";
import EmailTemplate from "./pages/EmailTemplate";
import RestaurantMenu from "./pages/RestaurantMenu";
import EcommerceListing from "./pages/EcommerceListing";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="/mobile-signup" element={<MobileSignup />} />
          <Route path="/email-template" element={<EmailTemplate />} />
          <Route path="/restaurant-menu" element={<RestaurantMenu />} />
          <Route path="/ecommerce-listing" element={<EcommerceListing />} />
          {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
