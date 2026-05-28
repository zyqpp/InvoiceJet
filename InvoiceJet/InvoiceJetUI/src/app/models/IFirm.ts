export interface IFirm {
  id: number;
  name: string;
  cui: string;
  regCom?: string | null;
  address: string;
  county: string;
  city: string;
}
