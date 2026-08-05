"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function QuickGenerate() {
  return (
    <Card className="bg-zinc-900 border-zinc-800 text-white">
      <CardHeader>
        <CardTitle>⚡ Quick Generate</CardTitle>
      </CardHeader>

      <CardContent className="space-y-4">
        <Input
          placeholder="Enter your reel topic..."
          className="bg-zinc-950 border-zinc-700"
        />

        <Button className="w-full">
          Generate with AI
        </Button>
      </CardContent>
    </Card>
  );
}