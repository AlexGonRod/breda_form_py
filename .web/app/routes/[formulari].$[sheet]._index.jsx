import {Fragment,useCallback,useContext,useEffect} from "react"
import {Button as RadixThemesButton,Container as RadixThemesContainer,Flex as RadixThemesFlex,Heading as RadixThemesHeading,Link as RadixThemesLink,Separator as RadixThemesSeparator,Spinner as RadixThemesSpinner,Text as RadixThemesText,TextField as RadixThemesTextField} from "@radix-ui/themes"
import {Link as ReactRouterLink} from "react-router"
import {Control as RadixFormControl,Field as RadixFormField,Label as RadixFormLabel,Message as RadixFormMessage,Root as RadixFormRoot} from "@radix-ui/react-form"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {ReflexEvent,getRefValue,getRefValues} from "$/utils/state"
import {jsx} from "@emotion/react"




function Spinner_d90a01b16ab0240f71e5f0d860e4b211 () {
  const reflex___state____state__formulari_app___pages___formulari___views___formulari____form_state = useContext(StateContexts.reflex___state____state__formulari_app___pages___formulari___views___formulari____form_state)



  return (
    jsx(RadixThemesSpinner,{loading:reflex___state____state__formulari_app___pages___formulari___views___formulari____form_state.loading_rx_state_},)
  )
}


function Button_42e80341543bf9868fdc4a8a2f283631 () {
  const reflex___state____state__formulari_app___pages___formulari___views___formulari____form_state = useContext(StateContexts.reflex___state____state__formulari_app___pages___formulari___views___formulari____form_state)



  return (
    jsx(RadixThemesButton,{css:({ ["isDisabled"] : reflex___state____state__formulari_app___pages___formulari___views___formulari____form_state.loading_rx_state_, ["width"] : "100%" }),radius:"small",type:"submit"},"Submit",jsx(Spinner_d90a01b16ab0240f71e5f0d860e4b211,{},))
  )
}


function Root_0ed1ebf75eb4b652f731d5a8fa65ea5c () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

    const handleSubmit_43c4d31d49e81fd67307541dfb94304a = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(ReflexEvent("reflex___state____state.formulari_app___pages___formulari___views___formulari____form_state.handle_submit", ({ ["data"] : form_data }), ({  })))], args, ({  }))))(ev));

        if (true) {
            $form.reset()
        }
    })
    


  return (
    jsx(RadixFormRoot,{className:"Root ",css:({ ["width"] : "100%", ["border"] : "1px solid", ["borderRadius"] : "10px", ["padding"] : "20px", ["spacing"] : "15px" }),onSubmit:handleSubmit_43c4d31d49e81fd67307541dfb94304a},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"column",gap:"3"},jsx(RadixFormField,{className:"Field ",css:({ ["display"] : "grid", ["marginBottom"] : "10px", ["width"] : "100%" }),name:"nom"},jsx(RadixFormLabel,{className:"Label ",css:({ ["fontSize"] : "24px", ["fontWeight"] : "bold", ["lineHeight"] : "35px", ["marginBottom"] : "16px" })},"Formulari del Concurs de paelles"),jsx(RadixThemesFlex,{css:({ ["width"] : "100%" }),direction:"column",gap:"1"},jsx(RadixFormLabel,{className:"Label ",css:({ ["fontSize"] : "15px", ["fontWeight"] : "500", ["lineHeight"] : "35px" })},"Nom"),jsx(RadixFormControl,{asChild:true,className:"Control "},jsx(RadixThemesTextField.Root,{pattern:"[A-Za-z]+",placeholder:"Nom i cognoms",radius:"small",required:true,type:"text"},)),jsx(RadixFormMessage,{className:"Message ",css:({ ["fontSize"] : "13px", ["opacity"] : "0.8", ["color"] : "red" }),match:"valueMissing"},"El nom \u00e9s obligatori"),jsx(RadixFormMessage,{className:"Message ",css:({ ["fontSize"] : "13px", ["opacity"] : "0.8", ["color"] : "orange" }),match:"patternMismatch"},"El nom no \u00e9s v\u00e0lid"))),jsx(RadixFormField,{className:"Field ",css:({ ["display"] : "grid", ["marginBottom"] : "10px", ["width"] : "100%" }),name:"telefon"},jsx(RadixThemesFlex,{css:({ ["width"] : "100%" }),direction:"column",gap:"1"},jsx(RadixFormLabel,{className:"Label ",css:({ ["fontSize"] : "15px", ["fontWeight"] : "500", ["lineHeight"] : "35px" })},"telefon"),jsx(RadixFormControl,{asChild:true,className:"Control "},jsx(RadixThemesTextField.Root,{pattern:"[0-9]{9}",placeholder:"Tel\u00e8fon",radius:"small",required:true,type:"text"},)),jsx(RadixFormMessage,{className:"Message ",css:({ ["fontSize"] : "13px", ["opacity"] : "0.8", ["color"] : "red" }),match:"valueMissing"},"El tel\u00e8fon \u00e9s obligatori"),jsx(RadixFormMessage,{className:"Message ",css:({ ["fontSize"] : "13px", ["opacity"] : "0.8", ["color"] : "orange" }),match:"patternMismatch"},"El tel\u00e8fon no \u00e9s v\u00e0lid"))),jsx(RadixFormField,{className:"Field ",css:({ ["display"] : "grid", ["marginBottom"] : "10px", ["width"] : "100%" }),name:"nombre"},jsx(RadixThemesFlex,{css:({ ["width"] : "100%" }),direction:"column",gap:"1"},jsx(RadixFormLabel,{className:"Label ",css:({ ["fontSize"] : "15px", ["fontWeight"] : "500", ["lineHeight"] : "35px" })},"persones"),jsx(RadixFormControl,{asChild:true,className:"Control "},jsx(RadixThemesTextField.Root,{placeholder:"Participants",radius:"small",required:true,type:"number"},)),jsx(RadixFormMessage,{className:"Message ",css:({ ["fontSize"] : "13px", ["opacity"] : "0.8", ["color"] : "red" }),match:"valueMissing"},"Aquest camp \u00e9s obligatori"),jsx(RadixFormMessage,{className:"Message ",css:({ ["fontSize"] : "13px", ["opacity"] : "0.8", ["color"] : "red" }),match:"typeMismatch"},"Aquest camp \u00e9s obligatori"))),jsx(Button_42e80341543bf9868fdc4a8a2f283631,{},)))
  )
}


export default function Component() {





  return (
    jsx(Fragment,{},jsx(RadixThemesContainer,{css:({ ["padding"] : "16px" }),size:"3"},jsx(RadixThemesFlex,{css:({ ["border"] : "1px solid", ["borderRadius"] : "10px", ["padding"] : "20px", ["marginBottom"] : "20px", ["width"] : "100%" }),direction:"column",gap:"1"},jsx(RadixThemesText,{align:"center",as:"p",css:({ ["margin"] : "" }),size:"9"},"\ud83e\udd58"),jsx(RadixThemesHeading,{align:"center",as:"h1",size:"8"},"Concurs de paelles"),jsx(RadixThemesHeading,{align:"center",as:"h2",css:({ ["marginBottom"] : "16px" }),size:"6"},"Breda de l'Eixample"),jsx(RadixThemesText,{as:"p"},"Si us plau, ompliu el formulari per participar en el concurs de paelles."),jsx(RadixThemesText,{as:"p"},"Qualsevol dubte, posseu-vos en contacte a: ",jsx(RadixThemesLink,{asChild:true,css:({ ["&:hover"] : ({ ["color"] : Object.assign(new String("var(--accent-8)"), ({ ["color"] : "accent", ["alpha"] : false, ["shade"] : 8 })) }) })},jsx(ReactRouterLink,{to:"mailto:bredainfocat@gmail.com"},"bredainfocat@gmail.com ")))),jsx(Root_0ed1ebf75eb4b652f731d5a8fa65ea5c,{},),jsx(RadixThemesSeparator,{size:"4"},)),jsx("title",{},"Formulari de la Breda"),jsx("meta",{content:"favicon.ico",property:"og:image"},))
  )
}