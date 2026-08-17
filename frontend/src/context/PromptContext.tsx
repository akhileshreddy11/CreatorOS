"use client";

import { createContext, useContext, useState, type ReactNode } from "react";

type PromptContextType = {
  prompt: string;
  setPrompt: (value: string) => void;
  platform: string;
  setPlatform: (value: string) => void;
  length: string;
  setLength: (value: string) => void;
  language: string;
  setLanguage: (value: string) => void;
  niche: string;
  setNiche: (value: string) => void;
  city: string;
  setCity: (value: string) => void;
  objective: string;
  setObjective: (value: string) => void;
  offer: string;
  setOffer: (value: string) => void;
  tone: string;
  setTone: (value: string) => void;
};

const PromptContext = createContext<PromptContextType | undefined>(undefined);

export function PromptProvider({ children }: { children: ReactNode }) {
  const [prompt, setPrompt] = useState("");
  const [platform, setPlatform] = useState("Instagram");
  const [length, setLength] = useState("Medium");
  const [language, setLanguage] = useState("en");
  const [niche, setNiche] = useState("Gyms");
  const [city, setCity] = useState("Hyderabad");
  const [objective, setObjective] = useState("Generate trial-class enquiries");
  const [offer, setOffer] = useState("Short videos, local offers, and approval-gated follow-up");
  const [tone, setTone] = useState("Helpful and local");

  return (
    <PromptContext.Provider
      value={{
        prompt,
        setPrompt,
        platform,
        setPlatform,
        length,
        setLength,
        language,
        setLanguage,
        niche,
        setNiche,
        city,
        setCity,
        objective,
        setObjective,
        offer,
        setOffer,
        tone,
        setTone,
      }}
    >
      {children}
    </PromptContext.Provider>
  );
}

export function usePrompt() {
  const context = useContext(PromptContext);

  if (!context) {
    throw new Error("usePrompt must be used inside PromptProvider");
  }

  return context;
}
