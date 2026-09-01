import { EmblemFree } from "@/components/ui/Emblem";

const COLUMNS = [
  {
    title: "Maison",
    links: [
      { label: "Collection", href: "#collection" },
      { label: "Manufacture", href: "#manufacture" },
      { label: "Mouvement", href: "#mouvement" },
    ],
  },
  {
    title: "Contact",
    links: [
      { label: "contact@meridian-watches.ch", href: "mailto:contact@meridian-watches.ch" },
      { label: "Journal", href: "#journal" },
    ],
  },
];

export function Footer() {
  return (
    <footer className="on-dark border-t border-[var(--color-hairline-dark)] bg-[var(--color-ink)] px-6 py-16 text-[var(--color-paper)] md:px-14">
      <div className="mx-auto flex max-w-7xl flex-col gap-12 md:flex-row md:justify-between">
        <div className="flex flex-col gap-4">
          <div className="flex items-center gap-3">
            <EmblemFree className="h-8 w-auto text-[var(--color-paper)]" />
            <span className="eyebrow">Meridian</span>
          </div>
          <p className="max-w-xs text-sm text-[var(--color-stone-light)]">
            L&apos;heure, rien de plus. Un mouvement, neuf cadrans, une garantie à vie.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-12 sm:gap-20">
          {COLUMNS.map((col) => (
            <div key={col.title}>
              <p className="eyebrow text-[var(--color-stone-light)]">{col.title}</p>
              <ul className="mt-4 flex flex-col gap-2">
                {col.links.map((link) => (
                  <li key={link.href}>
                    <a href={link.href} className="text-sm hover:text-[var(--color-accent-soft)]">
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="mx-auto mt-16 flex max-w-7xl flex-col gap-2 border-t border-[var(--color-hairline-dark)] pt-6 text-xs text-[var(--color-stone)] sm:flex-row sm:justify-between">
        <p>© {new Date().getFullYear()} Meridian Manufacture. Tous droits réservés.</p>
        <p className="eyebrow">Un mouvement. Neuf cadrans. Une vie.</p>
      </div>
    </footer>
  );
}
