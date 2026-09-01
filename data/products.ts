export type Product = {
  ref: string;
  slug: string;
  name: string;
  price: number;
  image: string;
  caseMaterial: string;
  dialType: string;
  complication?: string;
  diameter: string;
  powerReserve: string;
  waterResistance: string;
  glass: string;
};

export function productGallery(product: Product) {
  return [
    { src: product.image, label: "Face" },
    { src: `/images/product-${product.slug}-macro.svg`, label: "Macro cadran" },
    { src: `/images/product-${product.slug}-angle.svg`, label: "Profil boîtier" },
  ];
}

export function productMacro(product: Product) {
  return `/images/product-${product.slug}-macro.svg`;
}

export const CALIBRE = {
  name: "Calibre M.01",
  description:
    "Un seul mouvement, remonté et réglé à la main dans notre atelier. Neuf cadrans en sont l'unique variation — jamais le mécanisme.",
};

export const products: Product[] = [
  {
    ref: "01",
    slug: "anthracite",
    name: "Anthracite",
    price: 4200,
    image: "/images/product-anthracite.svg",
    caseMaterial: "Acier inoxydable brossé",
    dialType: "Cadran soleillé gris charbon",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé",
  },
  {
    ref: "02",
    slug: "given",
    name: "Given",
    price: 4200,
    image: "/images/product-given.svg",
    caseMaterial: "Acier inoxydable brossé",
    dialType: "Cadran laqué blanc craie",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé",
  },
  {
    ref: "03",
    slug: "meridien",
    name: "Méridien",
    price: 4600,
    image: "/images/product-meridien.svg",
    caseMaterial: "Acier inoxydable brossé",
    dialType: "Cadran guilloché bleu paon",
    complication: "Petite seconde",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé",
  },
  {
    ref: "04",
    slug: "aube",
    name: "Aube",
    price: 4200,
    image: "/images/product-aube.svg",
    caseMaterial: "Acier inoxydable brossé",
    dialType: "Cadran satiné champagne",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé",
  },
  {
    ref: "05",
    slug: "bruyere",
    name: "Bruyère",
    price: 4400,
    image: "/images/product-bruyere.svg",
    caseMaterial: "Acier inoxydable brossé",
    dialType: "Cadran texturé prune sourd",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé",
  },
  {
    ref: "06",
    slug: "silex",
    name: "Silex",
    price: 4600,
    image: "/images/product-silex.svg",
    caseMaterial: "Acier inoxydable brossé",
    dialType: "Cadran minéral gris silex",
    complication: "Petite seconde",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé",
  },
  {
    ref: "07",
    slug: "granit",
    name: "Granit",
    price: 4400,
    image: "/images/product-granit.svg",
    caseMaterial: "Acier inoxydable brossé",
    dialType: "Cadran grainé anthracite froid",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé",
  },
  {
    ref: "08",
    slug: "brume",
    name: "Brume",
    price: 4200,
    image: "/images/product-brume.svg",
    caseMaterial: "Acier inoxydable brossé",
    dialType: "Cadran opalin gris perle",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé",
  },
  {
    ref: "09",
    slug: "veille",
    name: "Veille",
    price: 4800,
    image: "/images/product-veille.svg",
    caseMaterial: "Acier inoxydable brossé, fond saphir",
    dialType: "Cadran noir profond, index appliqués",
    complication: "Petite seconde",
    diameter: "38 mm",
    powerReserve: "42 heures",
    waterResistance: "5 ATM",
    glass: "Verre saphir bombé, fond saphir",
  },
];
