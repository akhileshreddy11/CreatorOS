"use client";

type OutputToolbarProps = {
  onCopy?: () => void;
  onApprove?: () => void;
  onReject?: () => void;
  disabled?: boolean;
};

export default function OutputToolbar({ onCopy, onApprove, onReject, disabled = false }: OutputToolbarProps) {
  return (
    <div className="flex flex-wrap gap-3">
      <button type="button" onClick={onCopy} disabled={disabled} className="rounded-xl border border-zinc-700 px-4 py-2 text-sm font-semibold text-white hover:bg-zinc-800 disabled:opacity-50">Copy</button>
      <button type="button" onClick={onApprove} disabled={disabled} className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-500 disabled:opacity-50">Approve</button>
      <button type="button" onClick={onReject} disabled={disabled} className="rounded-xl border border-red-500/40 px-4 py-2 text-sm font-semibold text-red-300 hover:bg-red-500/10 disabled:opacity-50">Request revision</button>
    </div>
  );
}
