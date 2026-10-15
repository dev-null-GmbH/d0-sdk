import { EricClient } from "../dist/index.js";
const tenant = "11111111-1111-4111-8111-111111111111", product = "22222222-2222-4222-8222-222222222222";
const transport = {async request(url, options) {
  const path = new URL(url).pathname;
  if (path.endsWith("/notices")) return new Response(JSON.stringify({schema_version:"eric.user-notices.v1",version:"fixture",sdk_release:"fixture",documentation_archive_sha256:"0".repeat(64),license_document_sha256:"0".repeat(64),license_member:"license",notices:[]}),{status:200,headers:{"Content-Type":"application/json"}});
  if (path.endsWith("/simulations")) {const fixture=JSON.parse(options.body).fixture; return new Response(JSON.stringify({id:"33333333-3333-4333-8333-333333333333",fixture,status:"completed",outcome:fixture === "validation-accepted-v1" ? "simulated_accepted" : "simulated_rejected",simulated:true}),{status:202,headers:{"Content-Type":"application/json"}});}
  throw new Error(`unexpected offline route ${path}`);
}};
const prod=new EricClient("production",tenant,transport);
const notices=await prod.GetUserNotices({productId:product});
if(notices.schema_version!=="eric.user-notices.v1")throw new Error("notice fixture failed");
const test=new EricClient("test",tenant,transport);
for(const fixture of ["validation-accepted-v1","validation-rejected-v1"]){const result=await test.createEricTestSimulation({productId:product,idempotencyKey:`offline-${fixture}`,body:{fixture}});if(!result.simulated)throw new Error("simulation fixture failed");}
console.log("ERiC production read-only + both test simulations: offline fixtures passed");
